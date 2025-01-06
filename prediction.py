import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

st.title('Protein Structure Prediction')

def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon':{'color':'blue'}})
    pdbview.setBackgroundColor('#0E1117')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height = 500, width=800)

DEFAULT_SEQ = "MGIIAWIIFDLIAGIIAKLIMPGRDGGGFFLTCILGIVGAVVGGWLATMFGIGGSISGFNLHSFLVAVVGAILVLGIFRLLRRE"
txt = st.text_area('Input protein sequence', DEFAULT_SEQ, height=275)

def update(sequence=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence)
    name = sequence[:3] + sequence[-3:]
    pdb_string = response.content.decode('utf-8')

    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)

    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)

    st.subheader('3D Model of Predicted Protein Structure')
    render_mol(pdb_string)

    st.subheader('plDDT')
    st.write('The predicted local distance difference test (pLDDT) is a per-residue estimate of local confidence.')
    st.info(f'plDDT: {b_value}')

    st.download_button(
        label="Download PDB",
        data=pdb_string,
        file_name='predicted.pdb',
        mime='text/plain',
    )

predict = st.button('Predict', on_click=update)
