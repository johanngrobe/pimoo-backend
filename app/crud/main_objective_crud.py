from typing import List, Optional, Union

from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models import MainObjective
from app.schemas import MainObjectiveCreate, MainObjectiveUpdate


class CRUDMainObjective(CRUDBase[MainObjective, MainObjectiveCreate, MainObjectiveUpdate]):
    def __init__(self):
        super().__init__(MainObjective)

    def sort(
        self, 
        data: Union[List[MainObjective], MainObjective], 
        order_by: Optional[Column] = MainObjective.no, 
        ascending: bool = True
    ) -> Union[List[MainObjective], MainObjective]:
        """
        Sorts a list of MainObjective records or a single MainObjective by `no`, including sorting sub_objectives.
        """
        if isinstance(data, list):
            # Sort list of main objectives
            data.sort(key=lambda obj: getattr(obj, order_by.name), reverse=not ascending)
            
            # Sort sub_objectives within each main objective
            for instance in data:
                instance.sub_objectives.sort(key=lambda sub: sub.no)
        elif isinstance(data, MainObjective):
            # Sort only the sub_objectives of a single main objective
            data.sub_objectives.sort(key=lambda sub: sub.no)
        
        return data
    
    async def get_all_sorted(
        self, 
        db: AsyncSession, 
        municipality_id: Optional[int] = None,
        order_by: Optional[Column] = MainObjective.no, 
        ascending: bool = True
    ) -> List[MainObjective]:
        """
        Fetches and sorts MainObjective records.
        """
        # Fetch all records using get_all
        instances = await self.get_all(db, municipality_id)
        
        # Sort records using sort method
        return self.sort(instances, order_by=order_by, ascending=ascending)
    
    async def get_sorted(
        self,
        db: AsyncSession,
        id: int, 
        municipality_id: Optional[int] = None,
        order_by: Optional[Column] = MainObjective.no, 
        ascending: bool = True
    ) -> List[MainObjective]:
        """
        Fetches and sorts MainObjective records.
        """
        # Fetch all records using get_all
        instance = await self.get(db, id)
        # Sort records using sort method
        return self.sort(instance, order_by=order_by, ascending=ascending)
    


crud_main_objective = CRUDMainObjective()