from typing import (
    Any,
    Dict,
    List,
    Literal,
    Generic,
    Optional,
    Type,
    TypeVar,
    Tuple,
    Union,
)

from sqlalchemy import desc, asc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased, joinedload, RelationshipProperty, Query

from app.crud.exceptions import DatabaseCommitError, NotFoundError
from app.models.user import User

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
        data: Union[List[ModelType], ModelType],
        sort_params: List[
            Tuple[str, Union[str, Tuple[str, Union[str, Tuple[str, str]]]]]
        ],
    ) -> Union[List[ModelType], ModelType]:
        """
        Generalized sorting function for any object with support for deeply nested attributes.

        :param data: A single instance or a list of instances to sort.
        :param sort_params: List of tuples specifying sorting instructions:
                            - For main attributes: (field, "asc" or "desc")
                            - For nested attributes: (relationship, (field, "asc" or "desc"))
                            - Supports multi-level nesting.
        :return: The sorted data, with specified attributes sorted as per sort_params.
        """

        def sort_key(instance: Any, field: str, ascending: bool) -> Any:
            """Generate a sorting key based on a field and order."""
            value = getattr(instance, field, None)
            return (
                value
                if ascending
                else (-value if isinstance(value, (int, float)) else value)
            )

        def apply_nested_sorting(
            instance: Any, nested_sort_params: List[Tuple[str, Union[str, Tuple]]]
        ):
            """Recursively apply sorting to nested attributes."""
            for attr, sort_instruction in nested_sort_params:
                if isinstance(sort_instruction, tuple):
                    # Handle deeper nesting, e.g., "objectives.sub_objectives.no"
                    if isinstance(sort_instruction[1], tuple):
                        nested_attr, nested_sort_instruction = sort_instruction
                        nested_data = getattr(instance, attr, None)
                        if isinstance(nested_data, list):
                            # Sort the current level
                            field, order = nested_sort_instruction
                            ascending = order == "asc"
                            nested_data.sort(
                                key=lambda item: getattr(item, field),
                                reverse=not ascending,
                            )

                            # Recursively sort deeper levels
                            for item in nested_data:
                                apply_nested_sorting(
                                    item, [(nested_attr, nested_sort_instruction)]
                                )
                    else:
                        # Handle single-level nesting, e.g., "objectives.no"
                        field, order = sort_instruction
                        ascending = order == "asc"
                        nested_data = getattr(instance, attr, None)
                        if isinstance(nested_data, list):
                            nested_data.sort(
                                key=lambda item: getattr(item, field),
                                reverse=not ascending,
                            )

        # Main sorting function
        if isinstance(data, list):
            # If data is a list, apply top-level sorting
            for attr, sort_instruction in sort_params:
                if isinstance(sort_instruction, str):
                    # Top-level sorting
                    ascending = sort_instruction == "asc"
                    data.sort(key=lambda item: sort_key(item, attr, ascending))
                else:
                    # Nested attribute sorting (if it includes a tuple for deeper sorting)
                    for instance in data:
                        apply_nested_sorting(instance, [(attr, sort_instruction)])
        else:
            # If data is a single object, only apply nested sorting
            apply_nested_sorting(data, sort_params)

        return data

    async def get_all(
        self,
        db: AsyncSession,
        municipality_id: Optional[int] = None,
        sort_params: List[
            Tuple[str, Union[str, Tuple[str, Union[str, Tuple[str, str]]]]]
        ] = [],
        extra_fields: List[Any] = [],
    ) -> List[ModelType]:
        """
        Retrieve all records for the model, optionally filtering by municipality_id.
        """
        statement = select(self.model)
        statement = self.extend_statement(statement, extra_fields=extra_fields)

        if municipality_id is not None:
            statement = statement.where(self.model.municipality_id == municipality_id)

        result = await db.execute(statement)
        instances = result.scalars().all()

        if not instances:
            raise NotFoundError(self.model.__name__)

            # Apply recursive in-memory sorting for nested attributes
        instances = self.sort(instances, sort_params)

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
        sort_params: List[
            Tuple[str, Union[str, Tuple[str, Union[str, Tuple[str, str]]]]]
        ] = [],
        extra_fields: List[Any] = [],
    ) -> Optional[ModelType]:
        statement = select(self.model).where(getattr(self.model, key) == value)
        statement = self.extend_statement(statement, extra_fields=extra_fields)
        result = await db.execute(statement)
        instances = result.scalars().all()

        if not instances:
            raise NotFoundError(self.model.__name__, key, value)

            # Apply recursive in-memory sorting for nested attributes
        instances = self.sort(instances, sort_params)

        return instances

    async def get_by_multi_keys(
        self,
        db: AsyncSession,
        *,
        keys: Dict[str, Any],
        sort_params: List[
            Tuple[str, Union[str, Tuple[str, Union[str, Tuple[str, str]]]]]
        ] = [],
        extra_fields: List[Any] = [],
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
                        statement = statement.where(
                            getattr(current_model, attr) == value
                        )
            else:
                # Simple attribute (non-nested)
                statement = statement.where(getattr(self.model, key) == value)

        # Extend statement with any extra_fields for eager loading
        statement = self.extend_statement(statement, extra_fields=extra_fields)

        result = await db.execute(statement)
        instances = result.scalars().all()

        if not instances:
            raise NotFoundError(self.model.__name__, keys)

            # Apply recursive in-memory sorting for nested attributes
        instances = self.sort(instances, sort_params)

        return instances

    async def create(
        self, db: AsyncSession, obj_in: CreateSchemaType, user: Optional[User] = None
    ) -> ModelType:
        """Create a new record."""
        obj_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)

        if user:
            obj_data["municipality_id"] = user.municipality_id
            obj_data["created_by"] = user.id
            obj_data["last_edited_by"] = user.id

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
        association_fields: Dict[str, Tuple[Type[ModelType], str]],
    ) -> ModelType:
        # Create a copy of obj_in, excluding any association fields
        obj_in_data = obj_in.model_copy(
            deep=True, update={field: None for field in association_fields.keys()}
        )
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
        user: Optional[User] = None,
    ) -> ModelType:
        """Update a record by ID."""
        instance = await self.get(db, id)
        update_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)

        if user:
            update_data["last_edited_by"] = user.id

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
        association_fields: Dict[
            str, Tuple[Type[ModelType], str]
        ],  # {"tag_ids": (Tag, "tags"), "indicator_ids": (Indicator, "indicators")}
    ) -> Optional[ModelType]:

        # Create a copy of obj_in with association fields set to None
        obj_in_copy = obj_in.model_copy(
            deep=True, update={field: None for field in association_fields.keys()}
        )

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
