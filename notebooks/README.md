# Notebooks  
## The notebooks are work that each member of the data science team has contributed using a local environment and saved here to share.  

  
  Crucial parts of the project are contained in the notebooks.  
  
  [Snorkel](https://www.snorkel.org/blog/weak-supervision) is the process of "weak supervised" learning developed at Stanford in which tags are given to an unlabeled dataset. This is a cutting-edge technique that turns an unsupervised dataset into a supervised dataset. Once the dataset is labeled, we can start supervised learning using the Snorkel dataset as the training data. 
  
  The Category Prediction notebook contains the model that uses the Snorkel training dataset and predicts the types of police force used. The notebook offers two different ways to model the data. A Logistic Regression (lr) model or a Support Vector Machines (SVM) model can be placed into the [OneVsRestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsRestClassifier.html). Currently the SVM is being used since it included the most categories. Once the categories were created, tagged in a training dataset and reliably predicted on new data, we were able to use these tags to categorize the types of police force captured on social media.  
  One way to improve the outcomes of the tags is to start in the snorkel notebook, and add more keywords that are associated with each type of category of police force. This helps the training data become better, which will help the predictive model predict better. Take a look at the word frequencies visual in the Categories_Predictions notebook and see if those frequently found keywords are all placed into a category on the snorkel model. This is a good place to start in optimizing this these models.  
  
  The Twitter folder contains the code necessary to pull tweets directly from the Twitter API. Although our team decided to go a different direction and use agglomerated data, if you want to tac-on data directly from Twitter, the code is here.  
  
