export async function apiGet(path){
    const res = await fetch(`http://localhost:8000{path}`,{
        credentials: "include"
    });
    if(!res.ok) throw new Error(`${res.status} ${res.statusText}`);
}