from typing import Any, Dict, List, Literal, Generic, Optional, Type, TypeVar, Tuple

from sqlalchemy import asc, desc, Column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased, RelationshipProperty, joinedload

from app.models import User, Tag
from app.crud.exceptions import DatabaseCommitError, NotFoundError

# Define generic type variables for models and schemas
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

sorting_order = Literal["asc", "desc"]

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def extend_statement(
        self, statement: select, *, extra_fields: List[Any] = []
    ) -> select:
        for field in extra_fields:
            if (
                hasattr(field, "property")
                and isinstance(field.property, RelationshipProperty)
                and hasattr(self.model, field.key)
            ):
                statement = statement.options(joinedload(field))
        return statement
    
    def sort(
        self, 
        statement: Any, 
        sort_params: List[Dict[str, sorting_order]]
    ) -> Any:
        """
        Apply sorting to the statement based on sort_params.

        :param statement: The SQLAlchemy Select statement.
        :param sort_params: A list of dictionaries with column names as keys and sorting order ("asc" or "desc") as values.
        :return: The updated statement with sorting applied.
        """
        for sort_param in sort_params:
            for column_name, order in sort_param.items():
                column = getattr(self.model, column_name, None)
                if column is None or not isinstance(column, Column):
                    raise ValueError(f"Invalid column name '{column_name}' for sorting.")
                
                # Apply sorting order
                match order:
                    case "asc":
                        statement = statement.order_by(asc(column))
                    case "desc":
                        statement = statement.order_by(desc(column))
                    case _:
                        raise ValueError(f"Invalid sorting order '{order}' for column '{column_name}'.")

        return statement

    async def get_all(
            self, 
            db: AsyncSession, 
            municipality_id: Optional[int] = None,
            sort_params: Optional[List[Dict[str, sorting_order]]] = [],
            extra_fields: List[Any] = []
    ) -> List[ModelType]:
        """
        Retrieve all records for the model, optionally filtering by municipality_id.
        """
        statement = select(self.model)
        statement = self.extend_statement(statement, extra_fields=extra_fields)
        
        if municipality_id is not None:
            statement = statement.where(self.model.municipality_id == municipality_id)

        statement = self.sort(statement, sort_params)

        result = await db.execute(statement)
        instances = result.scalars().all()

        if not instances:
            raise NotFoundError(self.model.__name__)

        return instances

    async def get(
        self, db: AsyncSession, id: Any, extra_fields: List[Any] = []
    ) -> Optional[ModelType]:
        """Retrieve a single record by ID."""
        statement = select(self.model).where(self.model.id == id)
        statement = self.extend_statement(statement, extra_fields=extra_fields)
        result = await db.execute(statement)
        instance = result.scalars().first()

        if instance is None:
            raise NotFoundError(self.model.__name__, self.model.id)
        
        return instance
    
    async def get_by_key(
        self, 
        db: AsyncSession, 
        *, 
        key: str, 
        value: Any, 
        sort_params: Optional[List[Dict[str, sorting_order]]] = [],
        extra_fields: List[Any] = []
    ) -> Optional[ModelType]:
        statement = select(self.model).where(getattr(self.model, key) == value)
        statement = self.extend_statement(statement, extra_fields=extra_fields)
        statement = self.sort(statement, sort_params)
        result = await db.execute(statement)
        instance = result.scalars().all()

        if not instance:
            raise NotFoundError(self.model.__name__, key, value)
        
        return instance

    async def get_by_multi_keys(
        self,
        db: AsyncSession,
        *,
        keys: Dict[str, Any],
        sort_params: Optional[List[Dict[str, sorting_order]]] = [],
        extra_fields: List[Any] = []
    ) -> List[ModelType]:
        """
        Retrieves records matching multiple key-value pairs with optional query options,
        including filtering by nested relationships.

        Args:
            db (AsyncSession): The database session.
            keys (Dict[str, Any]): Dictionary of key-value pairs for filtering.
                Keys can be strings (attribute names) including nested relationships like "author.role".
            extra_fields (Optional[List[Any]]): Optional list of SQLAlchemy query options (e.g., joinedload).

        Returns:
            List[ModelType]: List of model instances matching the filters.
        """

        statement = select(self.model)
        alias_map = {}

        for key, value in keys.items():
            if value is None:
                continue

            # Split key to check for nested relationships (e.g., "author.role")
            nested_keys = key.split(".")
            if len(nested_keys) > 1:
                current_model = self.model
                for i, attr in enumerate(nested_keys):
                    if i < len(nested_keys) - 1:  # Intermediate relationships
                        # If alias doesn't exist, create it
                        if attr not in alias_map:
                            relationship_attr = getattr(current_model, attr)
                            alias = aliased(relationship_attr.property.mapper.class_)
                            alias_map[attr] = alias
                            statement = statement.join(alias, relationship_attr)
                        current_model = alias_map[attr]
                    else:
                        # Apply filter on the final attribute (e.g., "role")
                        statement = statement.where(getattr(current_model, attr) == value)
            else:
                # Simple attribute (non-nested)
                statement = statement.where(getattr(self.model, key) == value)

        # Extend statement with any extra_fields for eager loading
        statement = self.extend_statement(statement, extra_fields=extra_fields)
        statement = self.sort(statement, sort_params)

        result = await db.execute(statement)
        instances = result.scalars().all()

        if not instances:
            raise NotFoundError(self.model.__name__, keys)

        return instances
    
    async def create(
            self, 
            db: AsyncSession, 
            obj_in: CreateSchemaType, 
            user: Optional[User] = None
    ) -> ModelType:
        """Create a new record."""
        obj_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)
        
        if user:
            obj_data['municipality_id'] = user.municipality_id
            obj_data['created_by'] = user.id
            obj_data['last_edited_by'] = user.id

        new_instance = self.model(**obj_data)
        db.add(new_instance)

        try:
            await db.commit()
            await db.refresh(new_instance)
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)
        
        return new_instance
    
    async def create_with_associations(
        self, 
        db: AsyncSession, 
        obj_in: CreateSchemaType, 
        user: User,
        association_fields: Dict[str, Tuple[Type[ModelType], str]]
    ) -> ModelType:
        # Create a copy of obj_in, excluding any association fields
        obj_in_data = obj_in.model_copy(deep=True, update={field: None for field in association_fields.keys()})
        new_instance = await self.create(db, obj_in_data, user)

        # Handle each association field
        for field_name, (model, relationship_attr) in association_fields.items():
            ids = getattr(obj_in, field_name, None)
            if ids:
                # Fetch related instances by IDs
                stmt = select(model).where(model.id.in_(ids))
                result = await db.execute(stmt)
                related_instances = result.scalars().all()
                
                # Extend the specified relationship attribute on the new instance
                getattr(new_instance, relationship_attr).extend(related_instances)

        # Commit the associations
        try:
            await db.commit()
            await db.refresh(new_instance)
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)

        return new_instance

    async def update(
            self, 
            db: AsyncSession, 
            id: Any, 
            obj_in: UpdateSchemaType, 
            user: Optional[User] = None
    ) -> ModelType:
        """Update a record by ID."""
        instance = await self.get(db, id)
        update_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)

        if user:
            update_data['last_edited_by'] = user.id

        for field, value in update_data.items():
            setattr(instance, field, value)
        try:
            await db.commit()
            await db.refresh(instance)
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)
        
        return instance
    
    async def update_with_associations(
        self, 
        db: AsyncSession, 
        id: Any, 
        obj_in: UpdateSchemaType, 
        user: User,  # Replace `User` with the actual user type if necessary
        association_fields: Dict[str, Tuple[Type[ModelType], str]]  # {"tag_ids": (Tag, "tags"), "indicator_ids": (Indicator, "indicators")}
    ) -> Optional[ModelType]:

        # Create a copy of obj_in with association fields set to None
        obj_in_copy = obj_in.model_copy(deep=True, update={field: None for field in association_fields.keys()})

        # Update the main instance with user-specific context fields
        instance = await self.update(db, id, obj_in_copy, user)

        # Update each association field
        for field_name, (model, relationship_attr) in association_fields.items():
            ids = getattr(obj_in, field_name, None)
            if ids is not None:
                # Fetch the related instances based on IDs
                stmt = select(model).where(model.id.in_(ids))
                result = await db.execute(stmt)
                related_instances = result.scalars().all()

                # Replace the current relationship with the new instances
                setattr(instance, relationship_attr, related_instances)

        # Commit the updates
        try:
            await db.commit()
            await db.refresh(instance)
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)

        return instance
        

    async def delete(self, db: AsyncSession, id: Any) -> None:
        """Delete a record by ID."""
        instance = await self.get(db, id)
        try:
            await db.delete(instance)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)