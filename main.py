import pandas as pd
from deep_translator import GoogleTranslator
from flask import Flask
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from textblob import TextBlob

df = pd.read_csv("casas.csv")

colunas = ["tamanho", "preco"]
df = df[colunas]

X = df.drop("preco", axis=1)
y = df["preco"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

app = Flask(__name__)


# API
@app.route("/")
def home():
    return "Minha primeira API da Élyda."


@app.route("/sentimento/<frase>")
def sentimento(frase):
    tradutor = GoogleTranslator(source="pt", target="en")

    frase = "Python é ótimo para Machine Learning."
    frase_en = tradutor.translate(frase)

    tb = TextBlob(frase_en)

    polaridade = tb.sentiment.polarity

    return f"polaridade: {polaridade}"


@app.route("/cotacao/<int:tamanho>")
def cotacao(tamanho):
    preco = modelo.predict([[tamanho]])
    return str(preco)


app.run(debug=True)
