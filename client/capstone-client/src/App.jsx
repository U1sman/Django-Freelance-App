import BrowseGigs from "./pages/browseGigs";
import Login from "./pages/login";
import Signup from "./pages/signup";
import BrowseCategoryGigs from "./pages/BrowseCategoryGIgs";
import GigDetailedView from "./pages/gigDetailedView";

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';

function App() {

  const router = createBrowserRouter([
  {
    path:"/",
    element: <BrowseGigs/>
  },

  {
    path:"/login",
    element: <Login/>
  },

  {
    path:"/signup",
    element: <Signup/>
  },

  {
    path:"/category/:categoryName",
    element: <BrowseCategoryGigs/>
  },

  {
    path:"/gig/:gig_id",
    element: <GigDetailedView/>
  },

  ])

  return (
    <>
      <RouterProvider router={router}/>
    </>
  )
}

export default App
