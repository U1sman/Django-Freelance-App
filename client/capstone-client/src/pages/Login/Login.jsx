import React from 'react'
import { useState, useEffect } from 'react'
import { useNavigate } from "react-router-dom";

import { getCSRFToken} from '../../utils';
import { checkAuthenticatedStatus } from '../../apis';

const Login = () => {
  const [emailUsername, setEmailUsername]= useState("")
  const [password, setPassword]= useState("")
  const navigate = useNavigate()

    useEffect( () => {
      const redirectHomepage= async ()=>{
        const response = await checkAuthenticatedStatus()
        const isAuthenticated = response["isAuthenticated"]
        if (isAuthenticated === true){
          navigate("/")
        }
      }
      redirectHomepage()
    }, []);


  const login = async (event)=>{
      event.preventDefault();
  
      let userData= {
        emailUsername,
        password
      };
  
      let response = await fetch("http://127.0.0.1:8000/api/login/", {
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
    <div className="loginForm">
      <form>
        <h1>Login</h1>
        <input type="text" className="email-username_input" placeholder='enter username or email' onChange={(eu)=> setEmailUsername(eu.target.value)} value={emailUsername}/><br />
        <input type="password" className="password_input" placeholder='password' onChange={(p)=> setPassword(p.target.value)} value={password}/>

        <button onClick={login} className="submitLogin">Login</button>
      </form>
    </div>
    </>
  )
}

export default Login

