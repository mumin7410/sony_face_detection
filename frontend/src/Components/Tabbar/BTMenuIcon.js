import React from "react";

export default function BTMenuIcon({icon,text}){
    return(
        <>
            <div className="flex flex-col items-center">
                <div className="rounded-[8px] bg-[#FFF] px-[10px] py-[12px] align-middle justify-center flex">
                    {icon}
                </div>
                <p className="mt-[4px] text-[10px] text-[#FFF]">{text}</p>
            </div>
        </>
    )
}