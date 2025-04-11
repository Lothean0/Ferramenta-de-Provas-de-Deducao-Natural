import { useState } from 'react';
import '../styles/PropositionLogicBody.css';

function PropositionLogicBody() {
    const [proofSteps] = useState([
        {
            "status": null,
            "name": "Woman",
            "accOrder": 0,
            "parentId": null,
            "child": [
                {
                    "status": null,
                    "name": "Shoes",
                    "accOrder": 0,
                    "parentId": 1,
                    "child": [
                        {
                            "createdBy": null,
                            "status": null,
                            "name": "Good Sneckers",
                            "accOrder": 1,
                            "parentId": 5,
                            "child": []
                        },
                        {
                            "status": null,
                            "name": "Sneckers",
                            "accOrder": 1,
                            "parentId": 3,
                            "child": [
                                {
                                    "createdBy": null,
                                    "status": null,
                                    "name": "Good Sneckers",
                                    "accOrder": 1,
                                    "parentId": 5,
                                    "child": []
                                },
                                {
                                    "status": null,
                                    "name": "Bad Snackers",
                                    "accOrder": 2,
                                    "parentId": 5,
                                    "child": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "status": null,
                    "name": "Bijoux",
                    "accOrder": 1,
                    "parentId": 1,
                    "child": [
                        {
                            "status": null,
                            "name": "Sneckers_2",
                            "accOrder": 1,
                            "parentId": 3,
                            "child": [
                                {
                                    "createdBy": null,
                                    "status": null,
                                    "name": "Good Sneckers_2",
                                    "accOrder": 1,
                                    "parentId": 5,
                                    "child": []
                                },
                                {
                                    "status": null,
                                    "name": "Bad Snackers_2",
                                    "accOrder": 2,
                                    "parentId": 5,
                                    "child": []
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]);

    const renderTree = (nodes) => {
        if (!nodes || nodes.length === 0) return null;

        return (
            <div className="tree-level">
                {nodes.map((node, index) => (
                    <div key={index} className="tree-node" style={{ fontSize: '1.2em', color: 'black', fontWeight: 'bold', margin: '0 20px' }}>
                        <div className="node-label">{node.name}</div>
                        {renderTree(node.child)}
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="proofbox">
            {renderTree(proofSteps)}
        </div>
    );
}

export default PropositionLogicBody;
