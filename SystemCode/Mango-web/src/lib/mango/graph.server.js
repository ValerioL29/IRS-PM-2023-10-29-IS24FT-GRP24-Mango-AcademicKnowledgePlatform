export async function fetchMangoGraphAPI(paperId) {
    const data = await fetch(`http://127.0.0.1:8000/paper/graph/${paperId}`, {
        method: 'GET'
    }).then(response => response.json()).catch(error => console.log(error));

    return {
        citations: data.citations,
        references: data.references
    };
}