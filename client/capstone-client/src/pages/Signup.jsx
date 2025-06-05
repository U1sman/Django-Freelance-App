import React from 'react'
import { useState, useEffect } from 'react'
import { useNavigate } from "react-router-dom";
import { getCSRFToken, checkAuthenticatedStatus } from '../utils';

const Signup = () => {

  const [username, setUsername]= useState("")
  const [email, setEmail]= useState("")
  const [firstname, setFirstname]= useState("")
  const [lastname, setLastname]= useState("")
  const [password, setPassword]= useState("")
  const navigate = useNavigate()

  // Redirect to the homepage if already authenticated/logged in
  const checkRedirect= async ()=>{
      const isAuthenticated = await checkAuthenticatedStatus()
      if (isAuthenticated === true){
        navigate("/")
      }
    }
    useEffect( () => {
      checkRedirect()
    }, []);

  const signUp = async (event)=>{
    event.preventDefault();

    let userData= {
      username,
      email,
      firstname,
      lastname, 
      password
    };

    let response = await fetch("http://127.0.0.1:8000/api/signup/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      //data being sent 
      body: JSON.stringify(userData),
      credentials: 'include',
    })

    const result = await response.json()

    if (response.ok){
      // localStorage.setItem("currentuser-info", JSON.stringify(result["user_info"]))
      navigate("/")
    }
    else{
      alert(JSON.stringify(result))
    }
  }  
  
  return (
    <>

    <div className="signupform">
        <form>
            <h1>Sign Up</h1>
            <input type="text" className="username_input" placeholder="Username" onChange={(u)=> setUsername(u.target.value)} value={username}/><br />
            <input type="email" className="email_input" placeholder="Email" onChange={(e)=> setEmail(e.target.value)} value={email}/><br />
            <input type="text" className="firstname_input" placeholder="Firstname" onChange={(f)=> setFirstname(f.target.value)} value={firstname}/>
            <input type="text" className="lastname_input" placeholder="Lastname" onChange={(l)=> setLastname(l.target.value)} value={lastname}/><br />
            <input type="password" className="password_input" placeholder="Password" onChange={(p)=> setPassword(p.target.value)} value={password}/>

            <button onClick={signUp} className="submitSignup">Sign Up</button>
        </form>
    </div>

    </>
  )
}

export default Signup

