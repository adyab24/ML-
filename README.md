# ML-
Synthesize ML
Steps pursued for implementation:

1.Problem statement:
Design a system that assists local pharmacies to find alternate medicines when the prescribed medicines are not available. The system should -Be able to identify prescribed medicines from the doctor’s prescription. -Suggest the names of alternate medicines with similar therapeutic effects. - Also, recommends online sources for purchasing them.

2. We broke down the problem statements into 4 parts: 
	- A web interface where the user can upload their medicines 
	- An OCR technology to help read the prescriptions
	- A medical dataset to search for medicine alternatives
	- An ML algorithm to search for similar medicines.

3. We used flask which is a lightweight framework to set up our website. The flask routes for handling the home page, image uploads, and direct medicine searches were set up.
   The code also has 4 different html files for the website interface.

4. We tried several OCR methods and ended up choosing the "Gemini Vision Pro API" and we set some configurations to make it work better (temperature, top_k, top_p, max_output_tokens).
Upon trial we found the OCR worked best when only the name of the medicine is entered, so we used cropper.js, an easy to implement and easy to use cropping tool. 

5. The dataset was taken after a google seach from kaggle. The dataset is called "A-Z Medicine Dataset of India" by Shudhanshu Singh and Vivek Tiwari.
Then the missing values were handled and we selected the relevant features.

6. Since the medicine's compositions were in two different columns we implemented TF-IDF vectorization on the medicine composition data to transform text data into a suitable form for machine learning. Furthermore Truncated SVD was used to reduce the dimensionality of the TF-IDF vectors, optimizing for faster similarity computations.

7. For the similarity search on the vectorised compositions, we used cosine similarity (imported from sklearn) which identified similar matches above a certain threshold.
We then set our code to give the top 5 similar medicines.

8. We also added an additional feature in the website where the user can enter the name of the medicine and search for the alternatives.

9. Future enhancements:
	- Try google cloud's vision API
	- Take care of minor OCR errors
	- Implement a better algorithm to search for the medicine returned by the OCR in the dataframe
	- UI improvement and upgrading





