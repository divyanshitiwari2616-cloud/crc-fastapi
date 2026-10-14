import pstats

from fastapi import Body, FastAPI, HTTPException, status

app = FastAPI()
shipments= {
    1270: {"weight": 12.5, "content": "wooden table", "status": "delivered"},
    1271: {"weight": 13.5, "content": "toys", "status": "pending"},
    1272: {"weight": 10.2, "content": "chair", "status": "shipped"},
    1273: {"weight": 5.1, "content": "books", "status": "pending"},
    1274: {"weight": 22.0, "content": "refrigerator", "status": "delivered"},
    1275: {"weight": 3.7, "content": "clothes", "status": "shipped"},
    1276: {"weight": 8.9, "content": "shoes", "status": "pending"},
    1277: {"weight": 15.0, "content": "monitor", "status": "delivered"},
    1278: {"weight": 6.3, "content": "keyboard", "status": "shipped"},
    1279: {"weight": 1.1, "content": "mouse", "status": "pending"},
}

@app.get("/shipments/{id:int}")
def get_by_id_weight(id:int, weight:float):
        if weight<0:
             raise HTTPException( status_code=pstats.HTTP_400_BAD_REQUEST,detail="Weight must be a positive number")
        if weight not in shipments.values():
             raise HTTPException( status_code=pstats.HTTP_404_NOT_FOUND,detail=f"Shipment with weight {weight} not found")
        if id not in shipments:
            raise HTTPException(status_code=pstats.HTTP_404_NOT_FOUND,detail=f"Shipment with id {id} not found")
        return shipments[id]

@app.get("/shipments/latest")
def get_latest_shipment():
    latest_id = max(shipments.keys())
    return shipments[latest_id]


@app.post("/new-shipment")
def new_shipment(weight : float= Body(...),
                 content:str= Body(...)):
    if weight <= 0:
        raise HTTPException(status_code=400, detail="Weight must be greater than 0")
    new_id = max(shipments.keys()) + 1
    newestshipment ={
        "weight":weight,
        "content": content,
        "status": "pending"
    }
    shipments[new_id] = newestshipment
    return shipments[new_id]

@app.put ("/update-shipment/")
def update_shipment(id:int , weight: float, content:str):
    if id not in shipments:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")
    shipments[id].update({"weight": weight, "content": content})
    return {"message":f"Shipment with id {id} updated successfully"}


@app.patch("/update-shipment/{id}")
def update_the_shipment(weight: float|None=Body(None), content: str|None=Body(None)):
    if id not in shipments:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")
    if weight is not None:
        shipments[id]["weight"] = weight
    if content is not None:
        shipments[id]["content"] = content
    return {"message": f"Shipment with id {id} updated successfully"}

@app.delete("/remove-shipment/{id}")
def remove_shipment(id:int):
    if id not in shipments:
        raise HTTPException(
            status_code=pstats.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found"
        )
    shipments.pop(id)
    return {"message": f"Shipment with id {id} deleted successfully"}


from schemas import Ship, ShipmentStatus, updateshipment  # noqa: I001, RUF100


@app.post("/create-shipment,response_model=Response")
def create_new_shipment(shipment: Ship):
    new_id = max(shipments)+1
    new_content={ 
        "weight" : shipment.weight,
        "content": shipment.content,
    }
    shipments.update({new_id: new_content})
    return {"message": f"Shipment created{shipments[new_content]}"}


@app.put("/update-shipment/{sid}")
def update_shipment(data:updateshipment,sid:int):  # noqa: F811
    if sid not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id {sid} not found")
    shipments[sid]={"id": sid,**data.model_dump(),"status": ShipmentStatus.Placed()}
    return shipments[sid]

@app.patch("/shipments/{shipment_id}")
def shipment_patch(shipment_id:int, shipment:updateshipment):
    if shipment_id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id {shipment_id} not found")
    existing_shipment=shipments[shipment_id]
    updated_shipment=existing_shipment.copy()
    updated_shipment.update(shipment.model_dump(exclude_unset=True))
    shipments[shipment_id]=updated_shipment
    return updated_shipment