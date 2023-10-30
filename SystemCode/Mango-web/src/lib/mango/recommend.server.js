export async function fetchMangoRecommendAPI(userId) {
    const data = await fetch(
        `http://127.0.0.1:8000/recommend/dual?user_id=${userId}&top_k=10`, {
            // mode: 'no-cors',
            method: 'GET',
        }
    ).then(response => response.json()).catch(error => {
        console.log("Error: ", error);
    });

    return data.papers;
}

export async function fetchMangoRecEmbeddingAPI(paperId) {
    const data = await fetch(
        `http://127.0.0.1:8000/recommend/specter/${paperId}`, {
            // mode: 'no-cors',
            method: 'GET',
        }
    ).then(response => response.json()).catch(error => {
        console.log("Error: ", error);
    });

    return data;
}
