
mkdir tmp
# mkdir tmp/models
# mkdir tmp/libraries

# copy relevant files and models
cp ../inference/main_inference.py tmp
cp ../dependencies/models/* tmp/models
# cp ../dependencies/libraries/* tmp/libraries

# manually add Helsinki model for example
# git lfs clone https://huggingface.co/Helsinki-NLP/opus-mt-en-fr tmp/models/opus-mt-en-fr/

docker build -t inference -f inference.Dockerfile .

# check exit code
echo $?

rm tmp/main_inference.py
# rm -rf tmp
