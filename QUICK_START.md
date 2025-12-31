# AI-Driven Infrastructure Generator - Quick Reference

## 🚀 Getting Started in 30 Seconds

```bash
# 1. Install
pip install -r backend/requirements.txt

# 2. Run Server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

# 3. Test
python test_backend.py
```

**Server URL:** http://127.0.0.1:8000  
**API Docs:** http://127.0.0.1:8000/docs

---

## 📡 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System health check |
| `/text` | POST | Generate infrastructure from text |
| `/edit/diagram` | POST | Edit via diagram interactions |
| `/edit/terraform` | POST | Edit via Terraform code |

---

## 💡 Example Usage

### Generate Infrastructure
```bash
curl -X POST http://127.0.0.1:8000/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Create a VPC with EC2 and RDS database"}'
```

### Edit Resource
```json
POST /edit/diagram
{
  "current_model_id": "model-v1",
  "operation": "update_resource_property",
  "resource_id": "ec2-web-1",
  "property_name": "instance_type",
  "value": "t2.large"
}
```

---

## 📁 Key Files

- `backend/main.py` - FastAPI application
- `backend/model.py` - Infrastructure model (SSOT)
- `backend/edits.py` - Edit operations
- `test_backend.py` - Test suite

---

## ✅ Status

**All Systems Operational** ✅

- ✅ Backend Server Running
- ✅ All Tests Passing
- ✅ Documentation Complete
- ✅ Ready for Use

---

For detailed information, see [USER_GUIDE.md](file:///C:/Users/Ridham%20Shah/.gemini/antigravity/brain/4f8722d1-ab08-401e-98cf-875cc8f26376/USER_GUIDE.md)
