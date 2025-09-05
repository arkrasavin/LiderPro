from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from shared_schemas.observer import ObserverOut, ObserverPatch
from ..core.deps import require_roles
from ..db.session import get_db
from ..models.observer import Observer

router = APIRouter(prefix="/api/observers", tags=["observers"])


@router.get("/{obs_id}", response_model=ObserverOut)
def get_observers(
        obs_id: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    get_obs = db.get(Observer, obs_id)
    if not get_obs:
        raise HTTPException(status_code=404, detail="Observer not found")

    return ObserverOut.model_validate(get_obs)


@router.patch("/{obs_id}", response_model=ObserverOut)
def patch_observer(
        obs_id: int, payload: ObserverPatch,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    get_obs = db.get(Observer, obs_id)
    if not get_obs:
        raise HTTPException(status_code=404, detail="Observer not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(get_obs, key, value)
        db.add(get_obs)
        db.commit()
        db.refresh(get_obs)

    return ObserverOut.model_validate(data)


@router.delete("/{obs_id}", status_code=204)
def delete_observer(
        obs_id: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    get_obs = db.get(Observer, obs_id)
    if not get_obs:
        raise HTTPException(status_code=404, detail="Observer not found")
    db.delete(get_obs)
    db.commit()


@router.get("", response_model=dict)
def list_observers(
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    rows = db.query(Observer).order_by(Observer.name).all()
    out = {
        "data": [ObserverOut.model_validate(row) for row in rows],
        "meta": {"total_count": len(rows)}
    }

    return out


@router.post("", response_model=ObserverOut, status_code=201)
def create_observer(
        payload: ObserverPatch,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    obj = Observer(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return ObserverOut.model_validate(obj)
