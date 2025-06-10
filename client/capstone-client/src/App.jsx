import BrowseGigs from "./pages/browseGigs";
import Login from "./pages/login";
import Signup from "./pages/signup";
import BrowseCategoryGigs from "./pages/BrowseCategoryGIgs";
import GigDetailedView from "./pages/GigDetailedView/GigDetailedView";
import OrderDetails from "./pages/OrderDetails/OrderDetails";

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

  {
    path:"/gig/:gig_id/orderDetails/:pricingOptionId",
    element: <OrderDetails/>
  },
  ])

  return (
    <>
      <RouterProvider router={router}/>
    </>
  )
}

export default App
