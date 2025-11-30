from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice


@pytest.mark.asyncio
async def test_get_invoices_empty(client: AsyncClient):
    response = await client.get("/api/v1/invoices/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_invoices_with_data(client: AsyncClient, db_session: AsyncSession):
    invoice1 = Invoice(customer="Customer A", amount=Decimal("100.00"), status="pending")
    invoice2 = Invoice(customer="Customer B", amount=Decimal("200.50"), status="paid")
    db_session.add_all([invoice1, invoice2])
    await db_session.commit()

    response = await client.get("/api/v1/invoices/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["customer"] == "Customer B"
    assert data[1]["customer"] == "Customer A"


@pytest.mark.asyncio
async def test_create_invoice_success(client: AsyncClient):
    invoice_data = {"customer": "Test Customer", "amount": "150.75", "status": "pending"}

    response = await client.post("/api/v1/invoices/", json=invoice_data)
    assert response.status_code == 201
    data = response.json()
    assert data["customer"] == "Test Customer"
    assert data["amount"] == "150.75"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_invoice_default_status(client: AsyncClient):
    invoice_data = {"customer": "Test Customer", "amount": "100.00"}

    response = await client.post("/api/v1/invoices/", json=invoice_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_create_invoice_invalid_amount(client: AsyncClient):
    invoice_data = {"customer": "Test Customer", "amount": "-50.00", "status": "pending"}

    response = await client.post("/api/v1/invoices/", json=invoice_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_invoice_invalid_status(client: AsyncClient):
    invoice_data = {"customer": "Test Customer", "amount": "100.00", "status": "invalid_status"}

    response = await client.post("/api/v1/invoices/", json=invoice_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_invoice_missing_customer(client: AsyncClient):
    invoice_data = {"amount": "100.00", "status": "pending"}

    response = await client.post("/api/v1/invoices/", json=invoice_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_invoice_missing_amount(client: AsyncClient):
    invoice_data = {"customer": "Test Customer", "status": "pending"}

    response = await client.post("/api/v1/invoices/", json=invoice_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_invoice_empty_customer(client: AsyncClient):
    invoice_data = {"customer": "", "amount": "100.00", "status": "pending"}

    response = await client.post("/api/v1/invoices/", json=invoice_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_invoice_zero_amount(client: AsyncClient):
    invoice_data = {"customer": "Test Customer", "amount": "0", "status": "pending"}

    response = await client.post("/api/v1/invoices/", json=invoice_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_invoices_ordering(client: AsyncClient, db_session: AsyncSession):
    invoice1 = Invoice(customer="First", amount=Decimal("100.00"), status="pending")
    db_session.add(invoice1)
    await db_session.commit()
    await db_session.refresh(invoice1)

    invoice2 = Invoice(customer="Second", amount=Decimal("200.00"), status="pending")
    db_session.add(invoice2)
    await db_session.commit()

    response = await client.get("/api/v1/invoices/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["customer"] == "Second"
    assert data[1]["customer"] == "First"