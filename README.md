duplicate_agent_numbers = SubCategory.objects.values('subcategory_name').annotate(count=Count('subcategory_name')).filter(count__gt=1)

# Loop through each duplicate agent number and delete the duplicate records
for subcategory_name in duplicate_agent_numbers:
    SubCategory.objects.filter(subcategory_name=subcategory_name['subcategory_name']).delete()