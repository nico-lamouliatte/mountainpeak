from fastapi import FastAPI, Depends, HTTPException

from app.database import Base, engine, SessionLocal
from app.models import Peak
from app.schemas import MountainPeak, MountainPeakCreateOrUpdate, MountainPeakOptional

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to Mountain Peak"}


@app.get("/peaks", response_model=list[MountainPeak])
async def get_peaks(db=Depends(get_db)) -> list[Peak]:
    """Get all peaks.

    This endpoint retrieves all mountain peaks from the database.

    Returns:
        A list of all mountain peaks.
    """
    return db.query(Peak).all()


@app.post("/peaks", response_model=MountainPeak)
async def create_peak(request: MountainPeakCreateOrUpdate, db=Depends(get_db)) -> Peak:
    """Create a new peak.

    This endpoint creates a new mountain peak in the database.

    Args:
        peak: The details of the new mountain peak.

    Returns:
        The details of the newly created mountain peak.
    """
    peak = Peak(**request.model_dump())
    db.add(peak)
    db.commit()
    db.refresh(peak)
    return peak


@app.get("/peaks/{peak_id}", response_model=MountainPeak)
async def get_peak(peak_id: int, db=Depends(get_db)) -> Peak:
    """Get a single peak.

    This endpoint retrieves a single mountain peak from the database.

    Args:
        peak_id: The ID of the mountain peak to retrieve.

    Returns:
        The details of the mountain peak.
    """
    if peak := db.query(Peak).filter(Peak.id == peak_id).first():
        return peak

    raise HTTPException(status_code=404, detail="Peak not found")


@app.put("/peaks/{peak_id}", response_model=MountainPeak)
async def update_peak(
    peak_id: int, peak: MountainPeakCreateOrUpdate, db=Depends(get_db)
) -> Peak:
    """Update a mountain peak.

    This endpoint updates the details of a mountain peak in the database.

    Args:
        peak_id: The ID of the mountain peak to update.
        peak: The updated details of the mountain peak.

    Returns:
        The updated details of the mountain peak.
    """
    if db.query(Peak).filter(Peak.id == peak_id).first():
        db.query(Peak).filter(Peak.id == peak_id).update(
            peak.model_dump(exclude_unset=True)
        )
        db.commit()
        return db.query(Peak).filter(Peak.id == peak_id).first()

    raise HTTPException(status_code=404, detail="Peak not found")


@app.patch(
    "/peaks/{peak_id}",
    response_model=MountainPeak,
    response_model_exclude_unset=True,
)
async def update_peak(
    peak_id: int, peak: MountainPeakOptional, db=Depends(get_db)
) -> Peak:
    """Update a mountain peak.

    This endpoint updates the details of a mountain peak in the database.

    Args:
        peak_id: The ID of the mountain peak to update.
        peak: The updated details of the mountain peak.

    Returns:
        The updated details of the mountain peak.
    """
    # raise NotImplementedError(f"print(type(request)) => {type(peak)}")

    db.query(Peak).filter(Peak.id == peak_id).update(
        peak.model_dump(exclude_unset=True)
    )
    db.commit()
    return db.query(Peak).filter(Peak.id == peak_id).first()


@app.delete("/peaks/{peak_id}", status_code=204)
async def delete_peak(peak_id: int, db=Depends(get_db)):
    """Delete a mountain peak.

    This endpoint deletes a mountain peak from the database.

    Args:
        peak_id: The ID of the mountain peak to delete.

    Returns:
        The details of the deleted mountain peak.
    """
    if peak := db.query(Peak).filter(Peak.id == peak_id).first():
        db.delete(peak)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Peak not found")


@app.get("/peaks_in_zone/", response_model=list[MountainPeak])
async def get_peaks_in_zone(
    lat_top: float,
    lng_top: float,
    lat_bottom: float,
    lng_bottom: float,
    db=Depends(get_db),
) -> list[Peak]:
    """Get peaks in a specific zone.

    This endpoint retrieves all mountain peaks within a specific geographical zone.

    Args:
        lat_top: The latitude of the top boundary of the zone.
        lng_top: The longitude of the top boundary of the zone.
        lat_bottom: The latitude of the bottom boundary of the zone.
        lng_bottom: The longitude of the bottom boundary of the zone.

    Returns:
        A list of mountain peaks within the specified zone.
    """
    return (
        db.query(Peak)
        .filter(
            Peak.lat <= lat_top,
            Peak.lat >= lat_bottom,
            Peak.lng <= lng_top,
            Peak.lng >= lng_bottom,
        )
        .all()
    )
