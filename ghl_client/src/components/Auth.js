import React from 'react'

const Auth = () => {
  return (
    <div>
        <div className='flex flex-col items-center w-screen h-screen'>
            <div className='w-1/2 mt-14 h-12'>
                <span>GHL Location ID</span>
                <input  placeholder='Enter GHL Location ID' className='w-full h-full shadow-xl border border-gray-300'/>
            </div>
            <div className='w-1/2 mt-14 h-12'>
                <span>GHL Private API Access Code</span>
                <input  placeholder='Enter GHL Private API Access Code' className='w-full h-full shadow-xl border border-gray-300'/>
            </div>
            <div className='md:flex m-14 md:gap-14'>
            <div>
                <button className='bg-blue-500 px-16 py-3  shadow-2xl rounded-md active:scale-90 transition-all ease-in-out' >Validate and Submit</button>
            </div>
            <div>
                <button className='bg-emerald-600 px-10 py-3 shadow-2xl rounded-md active:scale-90 transition-all ease-in-out' >Grab your GHL Access Code</button>
            </div>
            </div>
        </div>
    </div>
  )
}

export default Auth