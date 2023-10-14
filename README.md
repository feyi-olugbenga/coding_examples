To run this service you must:
1. install the requirements.txt file using pip install requirments.txt in your terminal
2. run the code through your IDE or with the command `python brightwheel_assessment.py`
    
When doing this I initially wanted to read in and manipulate all 3 data sources but I found that half way through the first
dataset I worked on (Oklahoma) that that was too big a project to do in 2 hours. I have a few regrets with this:
 - I should have reduced the amount of columns that I tried to map from the Oklahoma dataset to the output dataset. 32 columns for 3 datasets in 2 hours is a lot to take on.
 - The prompt didn't have the AWS bucket name and I spent too much time trying to read in the datasets from AWS and fixing the errors when reading them in from local. 
 I'm not sure if this was intended but the Oklahoma file cuts off in the middle of the last line and the Nevada file has a different encoding than the other 2
 - I did some stuff fast instead of efficient and did not cover many edge cases
 
I think for the long term there is a lot of room for improvement a few things that I thought of are:
- Having data definitions so I don't have to guess field locations as much like with license_number 
- Have more time with data to create a proper mappings and allow for data enrichment. For example use Zip code to get county from an API or extrapolate the age fields in the Texas dataset to come up with an ages_served column there. 
- Clean up how the database is updated
- Add error handling
- Create more functions for general column normalization. For example a function that can properly separate all aspects of an address

I appreciate you taking the time to go through this and look forward to your response.