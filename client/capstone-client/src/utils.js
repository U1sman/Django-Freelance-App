import { isValid, format } from "date-fns";


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

export const formatDateTime= (utcDate)=>{
  const dateObject = new Date(utcDate);
  const formattedDate = isValid(dateObject)
  ? format(dateObject, "MMM d, yyyy 'at' h:mm a") : "Unknown";
  return formattedDate
}