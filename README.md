## WINterview 
* intelligent mock interview software system designed for everyone
* real-time interaction with a virtual interviewer utilizing speech synthesize and recognition
* text analysis, emotion recognition, as well as blink detection
* customized feedback with  data visualization

### System sructure
* Django framework
* Frontend: HTML/CSS/Javascript
* Backend: Python
* Database: SQLite3
### Files
* Blink
  - Detect the blinking times by opencv and dlib
  - Implement the model refered from Real-Time Eye Blink Detection using Facial Landmarks(2016)
* Emotion
  - Recognize the user emotion, including angry, sad, happy, surprise, fear, and neutral by Tensorflow, Keras, and opencv
  - Implement the model refered from Real-time Convolutional Neural Networks for Emotion and Gender Classification(2017)
* GTTS
  - Randomize and shuffle the questions from database according to the job which user had chosen
  - Submit the users' reply and recorded videos to analyze and save the results in the database
* MockInterview
  - Django main settings 
* nlp
  - Analyze the answers in different aspects with several models
  - NLTK for preprocessing
  - Sentiment Analysis
    - Logistic Regression and SDGClassifier from sklearn linear model to classify word corpus from NLTK Twiitter
    - MultinomialNB and BernoulliNB from sklearn naive_bayes to calculate the result confidence percentage
  - Gensim
    - Create the model from the data corpus which crawling professional technology and finance terms from web by Selenium and Beautifulsoup 
    - Compare the user reply and self-defined keywords to compare the words similarity
  - Skip-Gram Model
    - Assist system to give questions that similar to the last reply from the user
    - Adopt Recurrent Neural Network to deal with the sequentialed data
  - Google Bert
    - Compare the similarity between answer and user reply thorugh Torch framework
  - Aggregate every aspect and visualize the customized results
* questions
  - Collect data to database as easier way for the system administrator
  - Use News API to crawl the famous companies' and industries' news
* users
  - Define pages relevant to personal account and news
* templates
  - Create and design web pages
