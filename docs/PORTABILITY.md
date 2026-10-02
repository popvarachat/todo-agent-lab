# Portability Design

## หลักการ
Todo/Planner ไม่ถูกผูกกับ Agent Logic โดยตรง

```
Provider Adapter
      |
Canonical Task Model
      |
Agent Rules / OI
      |
Human Gate
      |
Report or Write-back
```

## ตอนทดลอง
Microsoft Planner = Source of Truth / DB
Write-back = OFF
Authentication = Azure CLI login ของแต่ละผู้ใช้

## ส่งต่อให้คนอื่น
1. Copy โฟลเดอร์ TodoAgentLab
2. ให้ผู้ใช้ login Microsoft/Azure CLI ของตนเอง
3. Copy settings.example.json -> settings.json
4. ใส่ plan_id ของ Planner ตัวเอง
5. รัน run.ps1
6. ตรวจ output ก่อนเปิด Write-back

## Provider ที่เพิ่มภายหลังได้
- Microsoft Planner
- Microsoft To Do
- CSV / Excel
- SharePoint List
- REST API ภายใน

Agent ใช้ Canonical Task Model เดิม จึงไม่ต้องเขียน Use Case ใหม่ทั้งหมด
