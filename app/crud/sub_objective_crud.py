from typing import List, Union

from app.crud.base_crud import CRUDBase
from app.models import SubObjective
from app.schemas import SubObjectiveCreate, SubObjectiveUpdate


class CRUDSubObjective(CRUDBase[SubObjective, SubObjectiveCreate, SubObjectiveUpdate]):
    def __init__(self):
        super().__init__(SubObjective)

    def sort(
        self, 
        data: Union[List[SubObjective], SubObjective], 
        ascending: bool = True
    ) -> Union[List[SubObjective], SubObjective]:
        """
        Sorts a list of SubObjective records or a single SubObjective by `MainObjective.no` first,
        and then by `SubObjective.no`.
        """
        def sort_key(sub_obj: SubObjective):
            # Sorting by MainObjective.no first, then by SubObjective.no
            return (sub_obj.main_objective.no, sub_obj.no)

        if isinstance(data, list):
            data.sort(key=sort_key, reverse=not ascending)
        elif isinstance(data, SubObjective):
            pass

        return data

crud_sub_objective = CRUDSubObjective()