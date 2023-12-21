import React, { useEffect, useState } from "react";
import Navbar from "../Components/Navbar/Navbar";
import BTTabbar from "../Components/Tabbar/BTTabbar";
import BTTransactionCard from "../Components/Card/BTTransactionCard";
import axios from 'axios';
export default function Transaction(){
    
    const [data, setData] = useState([]);
    useEffect(() => {
        const fetchData = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/Transaction');
            setData(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
        };

        fetchData();
    }, []);

    return(
        <>
        <div className='flex min-h-[100vh] bg-[#F5F8FF] font-Kanit'>
            <div className="flex flex-[0.1] items-center content-center justify-center">
                    <BTTabbar />
            </div>
            {/* main container */}
            <div className="w-full min-h-[100vh] bg-white rounded-[14px] mx-[20px] my-[40px] flex-[0.9] p-[30px]">
                {/* section_1 */}
                <div className="flex flex-row justify-between items-center">
                    <p className="text-[64px] font-Kanit text-[#1C1C1C]">Transaction</p>
                    <div className="flex flex-col items-center">
                        <p className="text-[#788AA3] text-[16px]">3/10/2023</p>
                        <p className="text-[#1C1C1C] text-[48px]">22:46</p>
                    </div>
                </div>
                {/* transactioncard section */}
                <div className="flex flex-wrap">
                    {data.map((item) => (
                        <BTTransactionCard key={item.autoID}
                            Name={item.Name}
                            CameraNo={item.CameraNo}
                            DateTime={item.DateTime}
                            EmployeeID={item.EmployeeID}
                        />
                    ))}
                </div>
            </div>
        </div>
        </>
    )
}