    import React from 'react';
    import { useEffect, useState } from 'react';
    import { useParams, Link } from 'react-router-dom';
    import Navbar from '../../components/Navbar/Navbar';
    import CategoryScrollBar from '../../components/CategoryScrollBar/CategoryScrollBar';
    import styles from './GigDetailedView.module.scss'
    import { fetchGig } from '../../utils';

    const GigDetailedView = () => {

        const params = useParams();
        const [gig, setGig] = useState({});

        useEffect( () => { 
            const fetchData = async ()=>{
                const data = await fetchGig(Number(params.gig_id));
                setGig(data);
            }
            fetchData();
            
        }, [Number(params.gig_id)]);
        
        return (
        <>

        <Navbar/>
        <CategoryScrollBar/>
        
        <div className="gigview_container">
            <p>in category/ <Link to={`/category/${gig.category?.name}`}>{gig.category?.name}</Link></p>
            <h2>{gig.title}</h2>
            <img src={`http://127.0.0.1:8000${gig.cover_image}`} alt="cover_image" />
            <h3>About this gig</h3>
            <p>{gig.description}</p>
            <div className="pricingPlan">
                {gig?.pricing_plan?.pricing_options.map((pricingOption)=>{
                    return(
                        <div className={styles.pricingOption} key={pricingOption.id}>
                            <p>type: {pricingOption.type}</p>
                            <p>price: {pricingOption.price}</p>
                            <p>description: {pricingOption.description}</p>
                            <p>delivery_time: {pricingOption.delivery_time}</p>
                            <Link to={`/gig/${gig.id}/orderDetails/${pricingOption.id}`}><button className="select">Select</button></Link>
                        </div>
                    )
                })}
            </div>
            <p>Get to know the Seller</p>
            <div className="sellerInfoBox">
                <img src={`http://127.0.0.1:8000${gig.related_seller?.profile_pic}`} alt="profile_pic" />
                <p>{gig.related_seller?.username}</p>
                <p>{gig.related_seller?.tagline}</p>
                <div className="ratingInfo">
                    this is a placeholder for the ratings and stuff
                </div>
                <p>from: {gig.related_seller?.country_name}</p>
                <p>Member Since: {gig.related_seller?.joined_date}</p>

            </div>
            <div className="ReviewSection">
                this is a placeholder for the review section
            </div>
        </div>

        </>
        )
    }

    export default GigDetailedView