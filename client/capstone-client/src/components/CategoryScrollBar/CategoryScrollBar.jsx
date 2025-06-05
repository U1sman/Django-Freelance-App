import { faDisplay } from '@fortawesome/free-solid-svg-icons';
import React from 'react'
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './CategoryScrollBar.module.css'

const CategoryScrollBar = () => {
    
    const [categories, setCategories] = useState([]);

    const fetchAllCategories = async () =>{
        let response = await fetch("http://127.0.0.1:8000/api/get_all_categories/", {
        method: 'GET',
        });
        let result = await response.json();
        setCategories(result)
    };

    useEffect( () => { fetchAllCategories() }, []);

  return (
    <>

        <div className={styles.categoriesContainer}>
        {categories.map((category) => {
            return (
            <div className="categoryCard" key={category.id}>
                <Link to={`/category/${category.name}`}>{category.name}</Link>
            </div>
            );
        })}
        </div>

    </>
  )
}

export default CategoryScrollBar