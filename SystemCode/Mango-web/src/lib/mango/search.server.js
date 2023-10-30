export async function fetchMangoSearchAPI(searchToken) {
    const response = await fetch(
        `http://127.0.0.1:8000/search/towhee?token=${searchToken}`, {
            // mode: 'no-cors',
            method: 'POST'
        }
    );
    
    const data = await response.json();

    return data.papers;
}
