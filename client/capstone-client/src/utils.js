export const getCSRFToken= ()=> {
  const cookies = document.cookie.split(';');
  // This just finds the value of the "csrftoken" cookie in your browser
  for (let cookie of cookies) {
    if (cookie.trim().startsWith('csrftoken=')) {
      return decodeURIComponent(cookie.trim().split('=')[1]);
    }
  }
  return null;
}


export const checkAuthenticatedStatus= async ()=>{
  let response = await fetch("http://127.0.0.1:8000/api/check_authenticated_status/", {
      method: 'GET',
      credentials: "include",
      });
      if (response.ok){
        let result = await response.json();
        return result["isAuthenticated"]
      }
      else{
        return false  
      }
}


export const fetchGig = async (gigId) =>{
      let response = await fetch(`http://127.0.0.1:8000/api/get_gig/${gigId}/`, {
      method: 'GET',
      });
      let result = await response.json();
      return result
  };
