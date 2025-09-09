from fastapi import APIRouter, Depends, Path
from app.domains.parts.schemas import PartCreate, PartUpdate, PartListResponse, PartOut
from app.schemas.common import UserInDB
from app.core.auth import get_current_user, require_role
from app.domains.parts import parts_logic

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.post(
    "/",
    response_model=PartOut,
    status_code=201,
    summary="Create a new part",
    description="Creates a new part in the inventory. Only accessible by admin users."
)
async def create_part(
    data: PartCreate,
    user: UserInDB = Depends(require_role("admin"))
):
    return await parts_logic.create_part_logic(data.model_dump(), user)

@router.get(
    "/",
    response_model=PartListResponse,
    summary="List all parts",
    description="Returns a list of all parts sorted by creation date."
)
async def get_all_parts(user: UserInDB = Depends(get_current_user)):
    return await parts_logic.get_all_parts_logic()

@router.get(
    "/{part_id}",
    response_model=PartOut,
    summary="Get part by ID",
    description="Retrieves a specific part by its ID."
)
async def get_part_by_id(
    part_id: str = Path(..., description="ID of the part to retrieve"),
    user: UserInDB = Depends(get_current_user)
):
    return await parts_logic.get_part_by_id_logic(part_id)

@router.patch(
    "/{part_id}",
    response_model=PartOut,
    summary="Update part",
    description="Updates a part's name or number. Only accessible by admin users."
)
async def update_part(
    part_id: str = Path(..., description="ID of the part to update"),
    data: PartUpdate = ...,
    user: UserInDB = Depends(require_role("admin"))
):
    return await parts_logic.update_part_logic(part_id, data.model_dump(exclude_unset=True), user)
