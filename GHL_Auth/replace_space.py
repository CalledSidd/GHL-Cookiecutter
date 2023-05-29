a = "contacts.readonly contacts.write locations.write locations.readonly locations/customFields.readonly locations/customFields.write locations/tags.write locations/tags.readonly businesses.readonly calendars.readonly calendars.write calendars/events.readonly calendars/events.write workflows.readonly users.readonly opportunities.readonly opportunities.write locations/tasks.readonly"

print(a.replace(' ', '%20'))
