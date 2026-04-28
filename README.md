# About:
This is a helper library for the AI-READI dataset, making some dataset access and interpretation more convenient. It probably deserves a full rewrite (spaghetti code), but I am planning on leaving it be because it gets the job done.

# Disclosures:
I'm a current AI-READI intern and trainee under grant OT20D032644

# Example of use:
```
import os
import helpers
import pandas as pd

# Point this to the folder containing your dataset
data_directory_path = "data"

# Now let's load the base patient data so we have something to build off of:
data = helpers.Dataset(data_directory_path)

# Now let's pick our survey question (Education, from https://docs.aireadi.org/v2/questionnaires/sdoh.pdf) from the OMOP table and give it a readable title:
survey_code_map = {
	'Edu_Level_123': 21493059, # Found by searching the online table 
    # (https://docs.aireadi.org/v3-omopAndClinicalTable) and using the 
    # TARGET_CONCEPT_ID from the entry for the question (not the answer choice)
}

# And now this should add a new column to data titled "Edu_Level_123" that includes the participants' answers to that survey question:
data = helpers.surveys(survey_code_map)

```
