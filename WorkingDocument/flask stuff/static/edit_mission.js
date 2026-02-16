const form = document.getElementById("missioncontent")
const update = document.getElementById("updatebutton")
const description = document.getElementById("question")

update.addEventListener("click", async (e) => {
    e.preventDefault();

    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get("id");

    const data = {"id":id, "question":description.value};

    try{
        const response = await fetch ("https://silver-halibut-9755xgqw64qxhp7rj-5000.app.github.dev/edit_mission?id="+id, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })

        const content = await response.json()
        console.log(content)
    }
    catch (error){
        console.log(error)
    }
})