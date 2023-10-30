export async function fetchMangoPaperAPI(paperId) {
    const response = await fetch(`http://127.0.0.1:8000/paper/details/${paperId}`, {
        method: "GET"
    }).catch(error => {
        console.log("Error: ", error);
    });
    const data = await response.json();

    return data;
}