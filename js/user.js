
export function login ({ username, password}) {
    return fetch ('' , {
        method: 'POST',
        method:{
            "content-Type": "application/json"
        },
        body:JSON.stringify({
            username,
            password
        })
    })

    .then(res=>{
        if (!res.ok) {
            console.log(res)
            throw new Error('Usuario y/o contraseña incorrectos')
        }

        return res.json()
    })

    .catch(e=> e)
}

export function register({
    username,
    email,
    firstname,
    lastname,
    password,
}){
    return fetch('',{
        method: "POST",
        body:JSON.stringify(
            {
                email,
                username,
                password,
                name:{
                    firstname,
                    lastname
                }
            }
        )
    })
    .then(res=>res.json())
    .then(json=>json)
    .catch(e=>e)
}