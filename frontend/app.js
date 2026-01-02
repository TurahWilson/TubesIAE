async function login(){
  const res = await fetch("http://localhost:8000/auth",{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify({
      query:`mutation{ login(username:"doctor",password:"123"){accessToken} }`
    })
  })
  console.log(await res.json())
}
