from flask import (
    Flask,
    render_template,
    request,
    Markup
    )

from flair.models import SequenceTagger
from flair.data import Sentence

app = Flask(__name__)

# On load le modèle dès que l'app se lance
MODEL = SequenceTagger.load("model/final-model.pt")
LABELS = {"<salaire>": "#F781F3", 
          "<complement_salaire>": "#5858FA"}

def generate_html_colored_text(text: str):
    """
    A partir d'un texte labelisé via flair,
    génère une balise html avec chaque mot labelisé 
    coloré selon la couleur su label
    """
    # html final fourni avec texte coloré
    final_html = "<a>"
    tokens = text.split(" ")
    for i in range(len(tokens)-1):
        # si le mot est suivi d'un label on le colore
        if tokens[i+1] in LABELS:
            final_html = final_html + " <span style='color: {0}'>{1}</span>"\
                .format(LABELS[tokens[i+1]], tokens[i])
            # on doit alors skipper le token suivant qui contient un label
            i += 2
        # sinon on l'ajoute simplement au html
        else:
            final_html = final_html + " <span style='color: #000000'>{0}</span>".format(tokens[i])
        
    # ajout fin balise
    final_html = final_html + " </a>"
    return final_html
    
@app.route("/")
def home():
    return render_template('home.html')
    
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':

        # ici on va chercher la description remplie par le user
        description = request.form['description']
        if description == '':
            return render_template('home.html', message='Please enter required fields')
        else:
            # on process la phrase avec le modele flair
            sentence = Sentence(description)
            MODEL.predict(sentence)
            sentence_str = sentence.to_tagged_string()
            # ajout des couleurs dans la phrase
            labeled_text = generate_html_colored_text(sentence_str)
            
            # creation balise couleurs labels
            labels_html = ""
            for label,color in LABELS.items():
                # on enleve les <> présents dans les labels
                # Flair pour ne pas péter le html
                label = label.replace("<","")
                label = label.replace(">","")
                labels_html += " <span style='color: {0}'>{1}</span>"\
                    .format(color, label)
            #print(labels_html)
            return render_template('processed.html', 
                                   processed_text=labeled_text,
                                   labels=labels_html)

@app.route('/restart', methods=['POST'])
def restart():
    if request.method == 'POST':        
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)