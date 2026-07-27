import re

with open("backend/ai_systems/service.py", "r") as f:
    content = f.read()

search = """        capability_map = []
        adoption_service = AdoptionRecordsService()

        for system in systems:
            # 1. Adoption Score (Average of all records for this system)
            adoption_records = await adoption_service.list_records(
                db=db,
                organization_id=organization_id,
                ai_system_id=system.id,
                limit=1000  # High enough limit to get all for the system
            )

            adoption_score = None
            if adoption_records:
                total_score = sum(record.adoption_score for record in adoption_records)
                adoption_score = total_score / len(adoption_records)"""

replace = """        capability_map = []
        adoption_service = AdoptionRecordsService()

        # Optimize N+1: Fetch all adoption records for the organization once
        all_adoption_records = await adoption_service.list_records(
            db=db,
            organization_id=organization_id,
            limit=10000
        )
        # Group records by ai_system_id
        adoption_by_system = {}
        for record in all_adoption_records:
            if record.ai_system_id not in adoption_by_system:
                adoption_by_system[record.ai_system_id] = []
            adoption_by_system[record.ai_system_id].append(record)

        for system in systems:
            # 1. Adoption Score (Average of all records for this system)
            system_adoption_records = adoption_by_system.get(system.id, [])

            adoption_score = None
            if system_adoption_records:
                total_score = sum(record.adoption_score for record in system_adoption_records)
                adoption_score = total_score / len(system_adoption_records)"""

if search in content:
    content = content.replace(search, replace)
    with open("backend/ai_systems/service.py", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Search string not found")
