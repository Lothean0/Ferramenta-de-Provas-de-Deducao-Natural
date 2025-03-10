import { useEffect, useState } from 'react';
import '../styles/PropositionLogicBody.css';
import axios from 'axios';
import ProofBox from './ProofBox';

function PropositionalLogicBody() {
    const [expression, setExpression] = useState("");
    const [rule, setRule] = useState("");

    async function sendExpressionAndRule() {
        if (!expression || !rule) {
            alert("Both expression and rule are required!");
            return;
        }

        try {
            const response = await axios.post("http://127.0.0.1:3000/api/checkExpression", {
                expression,
                rule
            });
            console.log("Server response:", response.data);
            window.confirm("Message sent successfully!");
            setExpression("");
            setRule("");
        } catch (error) {
            console.error("Error sending data:", error);
            alert("Failed to send data");
        }
    }

    return (
        <>
            <ProofBox />
        </>
    );
}

export default PropositionalLogicBody;


{/*
import { useState } from "react";

const PropositionalLogicBody = () => {
    const [proofs, setProofs] = useState([
        { id: 0, formula: "AND(A,B)", rule: null },
    ]);

    // Handles adding a new proof step
    const handleRuleSelect = (index, event) => {
        const rule = event.target.value;
        if (!rule) return;

        const newProof = {
            id: proofs.length,
            formula: `${rule}(${proofs[index].formula})`,
            rule: rule,
        };

        setProofs([...proofs, newProof]);
    };

    return (
        <div className="proofbox">
            <h2>Proof System</h2>
            {proofs.map((proof, index) => (
                <div key={proof.id} className="premisebox">
                    <div className="assumption">
                        {index === 0 && <span>with </span>}
                        <button className="assumption-btn">{index}: {proof.formula}</button>
                    </div>

                    <div className="proofbox">
                        <select
                            className="ruleselector"
                            onChange={(e) => handleRuleSelect(index, e)}
                        >
                            <option value="">Select rule...</option>
                            <optgroup label="Implication">
                                <option value="IMP-I">IMP-I</option>
                                <option value="IMP-E">IMP-E</option>
                            </optgroup>
                            <optgroup label="Conjunction">
                                <option value="AND-I">AND-I</option>
                                <option value="AND-E">AND-E</option>
                                <option value="AND-E1">AND-E1</option>
                                <option value="AND-E2">AND-E2</option>
                            </optgroup>
                        </select>
                    </div>

                    {proof.rule && (
                        <div className="formulabox">{proof.formula}</div>
                    )}
                </div>
            ))}
        </div>
    );
};

export default PropositionalLogicBody;
*/}

{/*
import React, { useState } from 'react';

function PropositionalLogicBody() {
  const [textInput, setTextInput] = useState('');
  const [response, setResponse] = useState('');

  const handleTextChange = (event) => {
    setTextInput(event.target.value);
  };

  const sendTextToOCaml = async () => {
    try {
      const result = await fetch('http://localhost:3000/process-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
      });

      const data = await result.json();
      setResponse(data.processedText);
    } catch (error) {
      console.error('Error sending text:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={textInput}
        onChange={handleTextChange}
        placeholder="Enter text"
      />
      <button onClick={sendTextToOCaml}>Send to OCaml</button>
      <p>Response: {response}</p>
    </div>
  );
}

export default PropositionalLogicBody;
*/}