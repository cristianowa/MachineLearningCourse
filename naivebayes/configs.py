#Database location

db_dir = "/home/cristiano/IMDB/"
db_dirs = {
"pos":db_dir + "/pos/",
"neg":db_dir + "/neg/"
}
start_file = 1#5
start_file = 5
end_file = 100#24004
end_file = 24004
#Vocabulary
load_from_file=True
vocabulary_file= db_dir + "imdb.vocab"
#Folding configuration
folds = 10
laplace_estimator=True



