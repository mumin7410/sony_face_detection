import React from "react";

export default function BTTransactionCard({
    EmployeeID,
    Name,
    DateTime,
    CameraNo,
    Image
}){
    const parseDateTime = (DateTime) => {
        return DateTime.split('T').join(' ')
    }
    return(
        <>
            {/* contaienr */}
            <div className="bg-white border-2 border-[#1C1C1C] px-[16px] py-[12px] inline-block rounded-[12px] m-[2px]">
                <div className="flex flex-row items-center">
                    <div>
                        <div className="w-[75px] h-[75px] rounded-[12px] bg-slate-700"></div>
                    </div>
                    <div className="ml-[8px]">
                        <p className="text-[12px] mb-[4px]">รหัสพนักงาน: {EmployeeID}</p>
                        <p className="text-[12px] mb-[4px]">ชื่อ: {Name}</p>
                        <p className="text-[12px]">วันที่ เวลา: {parseDateTime(`${DateTime}`)}</p>
                    </div>
                </div>
            </div>
        </>
    )
}