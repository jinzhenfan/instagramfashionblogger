Instagram Fashion Blogger App on Heroku. Recommendation system.

This is an Heroku app built on Flask. 
The original idea is to make customized recommendations of Instagram fashion bloggers through natural language processing. Whenever the user type in one fashion keyword in his/her mind, such as "party", "paris", or "shoes", this app will search in the blogger posts database for the best matches.  A word2vec deep learning neural network has been trained on a 15k-word casual corpus, and validated by a relational word benchmark. 
    A blogger corpus with 0.25 million words has been established by web scrapping. 1300 bloggers recommended by 500 fashion articles are included in this database.
Try the app at: https://instagram-blogger.herokuapp.com/



