import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './style.css'


// Komponen utama aplikasi
function App() {
  const [kondisi, setKondisi] = useState(null)
  const [loading, setLoading] = useState(false)
  const [host, setHost] = useState('')

  useEffect(() => {
    const ip = document.getElementById('host');
    setHost(ip.value)
  }, []);

  async function analize(el) {
    el.preventDefault()
    const formData = new FormData(el.currentTarget)
    setLoading(true)
    setKondisi(null)


    const request = await fetch(`http://${host}:8000/analyze`, {
      method: 'POST',
      body: formData,

    })
    const response = await request.json()
    setKondisi(response)
    setLoading(false)

  }

  function resetAll() {
    setKondisi(null)
  }

  return (
    <main className='sm:max-w-full flex-row mx-auto mt-5 rounded-sm mb-20 px-2'>
      <header className='flex-row text-center'>
        <h1 className='text-xl text-center pt-5 text-slate-700 font-semibold tracking-wider bg-gradient-to-r  from-teal-500 via-red-500 to-sky-500 text-transparent bg-clip-text'>Aplikasi Logika Fuzzy Pada Sistem Pakar Pariwisata</h1>
        <p className='text-slate-500 text-sm'>Made with 🖤️ by: Nur Kholis Setiawan</p>
      </header>
      <section className='mx-auto mt-5 sm:max-w-full md:max-w-[500px]'>
        <form action="" onSubmit={analize.bind(this)} className='w-full shadow-lg rounded-lg border px-5 py-6 grid grid-cols-1 gap-14'>
          <div className='relative'>
            <input type="number" className='form-control peer' name='budget' required id='budget' placeholder=' ' />
            <label for="budget" className='input-label'>Budget (Juta)</label>
          </div>
          <div className='relative'>
            <input type="number" className='form-control peer' name='jarak' required id='jarak' placeholder=' ' />
            <label for="jarak" className='input-label'>Jarak (Km)</label>
          </div>
          <div className='relative'>
            <input type="number" className='form-control peer' name='durasi' required id='durasi' placeholder=' ' />
            <label for="durasi" className='input-label'>Durasi (Jam)</label>
          </div>
          <div className='grid grid-cols-1 md:grid-cols-2 sm:gap-2 md:gap-4'>

            <button type="submit" className='btn-primary'>
              {loading &&
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>}
              <span>{loading ? 'Menganalisa' : 'Analisa'}</span></button><button type='reset' className='btn-danger' onClick={resetAll}>Reset</button>

          </div>
        </form>
      </section>
      <div className='max-w-[500px] mt-5 mb-10 mx-auto p-4'>
        {kondisi &&
          <>
            <p className='text-slate-600'>Persentase Kemungkinan: <span className='text-sky-700 inline-block'>{kondisi[0].persentase}%</span></p>
            <img src={`data:image/png;base64,${kondisi[0].path_graph}`} alt="Graphics" className='w-full' />
          </>
        }
      </div>

    </main>
  );
}

// Render aplikasi React ke dalam elemen dengan id "root"

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
