import React, { useState } from 'react';
import { saveAs } from 'file-saver';
import { read, utils } from 'xlsx';
import { useDropzone } from 'react-dropzone';
import Draggable from 'react-draggable';
import JSZip from 'jszip';
import jsPDF from 'jspdf';

function CertificatePreview({ frente, textElements, onTextMove, onTextChange }) {
  return (
    <div style={{ position: 'relative' }}>
      <img src={frente} alt="Frente do Certificado" style={{ width: '100%', height: 'auto' }} />

      {textElements.map((element, index) => (
        <Draggable key={index} defaultPosition={{ x: element.x, y: element.y }} onStop={(e, data) => onTextMove(index, data)}>
          <div style={{ position: 'absolute', left: element.x, top: element.y }}>
            <input
              type="text"
              value={element.text}
              onChange={(e) => onTextChange(index, e.target.value)}
            />
          </div>
        </Draggable>
      ))}
    </div>
  );
}

function App() {
  const [frente, setFrente] = useState(null);
  const [verso, setVerso] = useState(null);
  const [dados, setDados] = useState(null);
  const [textElements, setTextElements] = useState([]);

  const handleTextMove = (index, data) => {
    const updatedTextElements = [...textElements];
    updatedTextElements[index].x = data.x;
    updatedTextElements[index].y = data.y;
    setTextElements(updatedTextElements);
  };

  const onDropFrente = (acceptedFiles) => setFrente(acceptedFiles[0]);
  const onDropVerso = (acceptedFiles) => setVerso(acceptedFiles[0]);
  const onDropDados = (acceptedFiles) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const data = e.target.result;
      const workbook = read(data, { type: 'binary' });
      const rows = utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], { header: 1 });

      const headers = rows[0];
      const dados = rows.slice(1).map((row) => {
        return headers.reduce((obj, header, index) => {
          obj[header] = row[index];
          return obj;
        }, {});
      });

      setDados(dados);
    };

    reader.readAsBinaryString(acceptedFiles[0]);
  };

  const addTextElement = () => {
    setTextElements([...textElements, { text: 'Novo Texto', x: 50, y: 50 }]);
  };

  const handleTextChange = (index, newText) => {
    const updatedTextElements = [...textElements];
    updatedTextElements[index].text = newText;
    setTextElements(updatedTextElements);
  };

  const gerarCertificados = async () => {
    if (frente && verso && dados) {
      const zip = new JSZip();
  
      try {
        await Promise.all(
          dados.map(async (aluno, index) => {
            const pdf = new jsPDF();

            const frenteBase64 = await urlToBase64(frente);
            pdf.addImage(frenteBase64, 'JPEG', 10, 40, 100, 50);
  
            const versoBase64 = await urlToBase64(verso);
            pdf.addImage(versoBase64, 'JPEG', 10, 100, 100, 50);

            textElements.forEach((element) => {
              pdf.text(element.text, element.x, element.y);
            });
  
            zip.file(`certificado_${index + 1}.pdf`, await pdf.output('blob'));
          })
        );
  
        const content = await zip.generateAsync({ type: 'blob' });
        saveAs(content, 'certificados.zip');
      } catch (error) {
        console.error('Erro ao gerar certificados:', error);
      }
    }
  };  

  const urlToBase64 = async (url) => {
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    } catch (error) {
      console.error('Error converting image to base64:', error);
      throw error;
    }
  };

  const { getRootProps: getRootPropsFrente, getInputProps: getInputPropsFrente } = useDropzone({
    onDrop: onDropFrente,
    accept: 'image/*',
  });

  const { getRootProps: getRootPropsVerso, getInputProps: getInputPropsVerso } = useDropzone({
    onDrop: onDropVerso,
    accept: 'image/*',
  });

  const { getRootProps: getRootPropsDados, getInputProps: getInputPropsDados } = useDropzone({
    onDrop: onDropDados,
    accept: '.xlsx, .xls',
  });

  return (
    <div>
      <h1>Gerador de Certificados</h1>

      <div {...getRootPropsFrente()} style={dropzoneStyle}>
        <input {...getInputPropsFrente()} />
        <p>Arraste e solte a imagem da frente ou clique para selecionar.</p>
      </div>

      <div {...getRootPropsVerso()} style={dropzoneStyle}>
        <input {...getInputPropsVerso()} />
        <p>Arraste e solte a imagem do verso ou clique para selecionar.</p>
      </div>

      <div {...getRootPropsDados()} style={dropzoneStyle}>
        <input {...getInputPropsDados()} />
        <p>Arraste e solte a planilha de dados (Excel) ou clique para selecionar.</p>
      </div>

      <CertificatePreview
        frente={frente}
        textElements={textElements}
        onTextMove={handleTextMove}
        onTextChange={handleTextChange}
      />

      <button onClick={addTextElement}>Adicionar Texto</button>

      {textElements.map((element, index) => (
        <Draggable key={index} defaultPosition={{ x: element.x, y: element.y }} onStop={(e, data) => handleTextMove(index, data)}>
          <div>
            <input
              type="text"
              value={element.text}
              onChange={(e) => handleTextChange(index, e.target.value)}
            />
          </div>
        </Draggable>
      ))}

      <button onClick={gerarCertificados}>Gerar Certificados</button>
    </div>
  );
}

const dropzoneStyle = {
  border: '2px dashed #cccccc',
  borderRadius: '4px',
  padding: '20px',
  textAlign: 'center',
  margin: '20px',
};

export default App;
