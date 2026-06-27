export const checkAuthenticatedStatus= async ()=>{
  let response = await fetch("http://127.0.0.1:8000/api/check_authenticated_status/", {
      method: 'GET',
      credentials: "include",
      });
      if (response.ok){
        let result = await response.json();
        return {"isAuthenticated": result['isAuthenticated'], "currentUser": result['current_user']}
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


export const fetchOrder = async (orderId) =>{
   let response = await fetch(`http://127.0.0.1:8000/api/get_order/${orderId}/`, {
    method: 'GET',
   });
   let result = await response.json();
   return result
};


export const fetchAllOrderDeliveries = async(orderId) =>{
   let response = await fetch(`http://127.0.0.1:8000/api/get_all_order_deliveries/${orderId}/`, {
    method: 'GET',
   });
   let result = await response.json();
   return result
}