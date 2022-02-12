import React, { useEffect, useState } from 'react'

function addZero(i) {
    if (i < 10) { i = "0" + i }
    return i;
}

export const Room = ({ room }) => {
    var startTime = room.start_time === 'none' ? null : new Date(room.start_time)
    const [time, setTime] = useState("")

    useEffect(() => {
        if (startTime) {
            setInterval(() => {
                updateDuration()
            }, 1000)
        }
    }, [])

    const updateDuration = () => {
        const now = Date.now()
        const dif = (now - startTime) / 1000;
        const min = parseInt(dif / 60);
        const second = parseInt(dif % 60);
        const temp = `${min < 10 ? '0' : ''}${min}:${second < 10 ? '0' : ''}${second}`
        setTime(temp)
    }

    return (
        <div className={`restroom-card ${room.available ? 'free' : 'busy'}`}>
            {room.number}
            <div className='status'>ห้อง{!room.available && 'ไม่'}ว่าง</div>
            {startTime &&
                <>
                    <div className="enter-time">
                        เวลาที่เข้า {startTime.getHours()}:{addZero(startTime.getMinutes())} น.
                    </div>
                    <div className="duration">
                        เข้าไปแล้ว {time} นาที
                    </div>
                </>
            }
        </div >
    )
}

export default Room
