-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 13 Feb 2022 pada 20.04
-- Versi server: 10.4.20-MariaDB
-- Versi PHP: 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `perpustakaan1`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `buku`
--

CREATE TABLE `buku` (
  `id_buku` varchar(150) NOT NULL,
  `judul_buku` varchar(75) NOT NULL,
  `pengarang` varchar(50) DEFAULT NULL,
  `penerbit` varchar(50) DEFAULT NULL,
  `tahun_terbit` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `buku`
--

INSERT INTO `buku` (`id_buku`, `judul_buku`, `pengarang`, `penerbit`, `tahun_terbit`) VALUES
('37f0295d-b08b-4a5d-bfea-b1f53ba9067f', 'belajar geografi 2', 'hikmat hidayat', 'gramedia', 2020),
('4c0d7279-4d9c-4935-a28a-72f7bba0cbff', 'belajar matematika', 'hikmat hidayat', 'gramedia', 2015),
('b4fc1140-0994-4674-9d53-0892d3afd7ca', 'belajar kimiaa', 'devi nur', 'gramedia 2', 2017),
('bc3d5380-3703-435e-9e92-8a071c2998c4', 'belajar fisika', 'hikmat hidayat', 'gramedia', 2020);

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id_user` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(150) NOT NULL,
  `nama_lengkap` varchar(70) NOT NULL,
  `alamat` varchar(200) DEFAULT NULL,
  `role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id_user`, `username`, `email`, `password`, `nama_lengkap`, `alamat`, `role`) VALUES
('42ceb784-7add-49d7-b235-e2062ea1ffb4', 'ridwan3', 'ridwan2@gmail.com', '12345678', 'ridwan purnama sakti', 'cikole bandung barat', 'user'),
('6c3dcb17-4802-458a-9e40-392e7f61f757', 'admin', 'admin@gmail.com', 'admin', 'hikmat hidayat', 'Bandung', 'admin'),
('e0404730-4fcd-41cf-bac6-2e5590cf38fe', 'hikmat', 'hikmat6@gmail.com', '8D969EEF6ECAD3C29A3A629280E686CF0C3F5D5A86AFF3CA12', 'Hikmat Hidayat', 'Cinunuk', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `buku`
--
ALTER TABLE `buku`
  ADD PRIMARY KEY (`id_buku`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
