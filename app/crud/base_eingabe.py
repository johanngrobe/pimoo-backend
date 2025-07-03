from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.services.pdf import BasePDF

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDEingabe(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    # def __init__(self, model: Type[ModelType]):
    #     super().__init__(model)

    def detach_instance(self, instance: Any, exclude: Optional[List[str]] = []) -> Any:
        """
        Creates a detached copy of a SQLAlchemy instance, excluding specified columns.

        :param instance: The SQLAlchemy instance to detach.
        :param exclude: An optional list of column names to exclude from the copied instance.
        :return: A detached copy of the instance.
        """
        instance_copy = instance.__class__(
            **{
                c.key: getattr(instance, c.key)
                for c in inspect(instance).mapper.column_attrs
                if c.key not in exclude
            }
        )

        # Optionally set specific columns to None if included in exclude
        for column in exclude:
            if hasattr(instance_copy, column):
                setattr(instance_copy, column, None)

        return instance_copy

    async def copy_nested(
        self,
        instance: Any,
        copied_instance: Any,
        nested_attrs: Dict[str, List[str]],
        exclude: Optional[List[str]] = [],
    ) -> None:
        """
        Recursively copies nested attributes from the instance to the copied instance.

        :param instance: The original SQLAlchemy instance.
        :param copied_instance: The detached copy of the original instance.
        :param nested_attrs: A dictionary where keys are attribute names representing nested data structures
                             and values are lists of further nested attributes to copy within each item.
        :param exclude: A list of column names to exclude when detaching nested instances.
        """
        for attr, sub_attrs in nested_attrs.items():
            nested_items = getattr(instance, attr, None)
            if nested_items is None:
                continue

            copied_items = []
            for item in nested_items:
                copied_item = self.detach_instance(item, exclude=exclude)
                setattr(
                    copied_item, "submission", copied_instance
                )  # Set parent reference

                # Recursively copy sub-nested items if sub-attributes are provided
                if sub_attrs:
                    await self.copy_nested(
                        item,
                        copied_item,
                        {sub_attr: [] for sub_attr in sub_attrs},
                        exclude,
                    )
                copied_items.append(copied_item)

            setattr(copied_instance, attr, copied_items)

    async def copy(
        self,
        db: AsyncSession,
        id: int,
        updates: Optional[Dict[str, Union[int, bool]]] = None,
        exclude: Optional[List[str]] = [],
        nested_attributes: Dict[str, List[str]] = {},
    ) -> Any:
        """
        Copies a submission by ID, including any nested attributes specified, and assigns new ownership.

        :param db: The database session.
        :param id: The ID of the submission to copy.
        :param user: The user to assign as the creator and last editor of the copied submission.
        :param exclude: An optional list of column names to exclude when detaching the instance.
        :param nested_attributes: A dictionary where keys are attribute names representing nested data structures
                                and values are lists of further nested attributes to copy within each item.
        :param updates: A dictionary of attributes to update on the copied instance.
        :return: A copied submission instance.
        """

        # Fetch the original instance
        instance = await self.get(db, id)

        # Create a detached copy of the submission
        copied_instance = self.detach_instance(instance, exclude=exclude)

        # Apply updates to the copied instance if provided
        if updates:
            for attr, value in updates.items():
                setattr(copied_instance, attr, value)

        # Copy nested attributes if specified
        if nested_attributes:
            await self.copy_nested(
                instance, copied_instance, nested_attributes, exclude
            )

        # Add the copied instance to the session and commit
        db.add(copied_instance)
        await db.commit()
        await db.refresh(copied_instance)

        return copied_instance

    async def export(self, db: AsyncSession, id: int, PDF: BasePDF) -> bytes:
        instance = await self.get(db, id)
        pdf = PDF(orientation="P", unit="mm", format="A4")
        return pdf.export(instance)
