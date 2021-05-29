-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 29, 2021 at 12:40 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uasflask_32180050`
--

-- --------------------------------------------------------

--
-- Table structure for table `agents`
--

CREATE TABLE `agents` (
  `id` int(11) NOT NULL,
  `img` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL,
  `bio` varchar(255) NOT NULL,
  `a1` varchar(50) NOT NULL,
  `ai1` varchar(255) NOT NULL,
  `ad1` varchar(255) NOT NULL,
  `a2` varchar(50) NOT NULL,
  `ai2` varchar(255) NOT NULL,
  `ad2` varchar(255) NOT NULL,
  `a3` varchar(50) NOT NULL,
  `ai3` varchar(255) NOT NULL,
  `ad3` varchar(255) NOT NULL,
  `a4` varchar(50) NOT NULL,
  `ai4` varchar(255) NOT NULL,
  `ad4` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `agents`
--

INSERT INTO `agents` (`id`, `img`, `name`, `role`, `bio`, `a1`, `ai1`, `ad1`, `a2`, `ai2`, `ad2`, `a3`, `ai3`, `ad3`, `a4`, `ai4`, `ad4`, `created_at`, `updated_at`) VALUES
(70, 'uploads/agents/jett.png', 'Jett', 'Duelists', 'Representing her home country of South Korea, Jett\'s agile and evasive fighting style lets her take risks no one else can. She runs circles around every skirmish, cutting enemies up before they even know what hit them.', 'Updraft', 'uploads/agents/abilities/updraft.png', 'INSTANTLY propel Jett high into the air.', 'Tailwind', 'uploads/agents/abilities/tailwind.png', 'INSTANTLY propel Jett in the direction she is moving. If Jett is standing still, she will propel forward.', 'Cloudburst', 'uploads/agents/abilities/cloudburst.png', 'INSTANTLY throw a projectile that expands into a brief vision-blocking cloud on impact with a surface. HOLD the ability key to curve the smoke in the direction of your crosshair.', 'Blade Storm', 'uploads/agents/abilities/bladestorm.png', 'EQUIP a set of highly accurate throwing knives that recharge on killing an opponent. FIRE to throw a single knife at your target. ALTERNATE FIRE to throw all remaining daggers at your target.', '2021-05-29 08:46:50', '2021-05-29 08:49:36'),
(71, 'uploads/agents/raze.png', 'Raze', 'Duelists', 'Raze explodes out of Brazil with her big personality and big guns. With her blunt-force-trauma playstyle, she excels at flushing entrenched enemies and clearing tight spaces with a generous dose of boom.', 'Blast Pack', 'uploads/agents/abilities/blastpack.png', 'INSTANTLY throw a Blast Pack that will stick to surfaces. RE-USE the ability after deployment to detonate, damaging and moving anything hit.', 'Paint Shells', 'uploads/agents/abilities/paintshells.png', 'EQUIP a cluster grenade. FIRE to throw the grenade, which does damage and creates sub-munitions, each doing damage to anyone in their range.', 'Boom Bot', 'uploads/agents/abilities/boombot.png', 'EQUIP a Boom Bot. FIRE will deploy the bot, causing it to travel in a straight line on the ground, bouncing off walls. The Boom Bot will lock on to any enemies in its frontal cone and chase them, exploding for heavy damage if it reaches them.', 'Showstopper', 'uploads/agents/abilities/showstopper.png', 'EQUIP a rocket launcher. FIRE shoots a rocket that does massive area damage on contact with anything.', '2021-05-29 08:55:38', '2021-05-29 08:55:38'),
(72, 'uploads/agents/breach.png', 'Breach', 'Initiators', 'The bionic Swede Breach fires powerful, targeted kinetic blasts to aggressively clear a path through enemy ground. The damage and disruption he inflicts ensures no fight is ever fair.', 'Flashpoint', 'uploads/agents/abilities/flashpoint.png', 'EQUIP a blinding charge. FIRE the charge to set a fast-acting burst through the wall. The charge detonates to blind all players looking at it.', 'Fault Line', 'uploads/agents/abilities/faultline.png', 'EQUIP a seismic blast. HOLD FIRE to increase the distance. RELEASE to set off the quake, dazing all players in its zone and in a line up to the zone.', 'Aftershock', 'uploads/agents/abilities/aftershock.png', 'EQUIP a fusion charge. FIRE the charge to set a slow-acting burst through the wall. The burst does heavy damage to anyone caught in its area.', 'Rolling Thunder', 'uploads/agents/abilities/rollingthunder.png', 'EQUIP a Seismic Charge. FIRE to send a cascading quake through all terrain in a large cone. The quake dazes and knocks up anyone caught in it.', '2021-05-29 08:59:21', '2021-05-29 08:59:21'),
(73, 'uploads/agents/cypher.png', 'Cypher', 'Sentinels', 'The Moroccan information broker, Cypher is a one-man surveillance network who keeps tabs on the enemy\'s every move. No secret is safe. No maneuver goes unseen. Cypher is always watching.', 'Cyber Cage', 'uploads/agents/abilities/cybercage.png', 'INSTANTLY toss the cyber cage in front of Cypher. ACTIVATE to create a zone that blocks vision and plays an audio cue when enemies pass through it', 'Spycam', 'uploads/agents/abilities/spycam.png', 'EQUIP a spycam. FIRE to place the spycam at the targeted location. RE-USE this ability to take control of the camera\'s view. While in control of the camera, FIRE to shoot a marking dart. This dart will reveal the location of any player struck by the dart.', 'Trapwire', 'uploads/agents/abilities/trapwire.png', 'EQUIP a trapwire. FIRE to place a destructible and covert tripwire at the targeted location, creating a line that spans between the placed location and the wall opposite. Enemy players who cross a tripwire will be tethered, revealed, and dazed after a sho', 'Neural Theft', 'uploads/agents/abilities/neuraltheft.png', 'INSTANTLY use on a dead enemy player in your crosshairs to reveal the location of all living enemy players.', '2021-05-29 09:10:23', '2021-05-29 09:10:23'),
(74, 'uploads/agents/sova.png', 'Sova', 'Initiators', 'Born from the eternal winter of Russia\'s tundra, Sova tracks, finds, and eliminates enemies with ruthless efficiency and precision. His custom bow and incredible scouting abilities ensure that even if you run, you cannot hide.', 'Shock Bolt', 'uploads/agents/abilities/shockbolt.png', 'EQUIP a bow with a shock bolt. FIRE to send the explosive bolt forward, detonating upon collision and damaging players nearby. HOLD FIRE to extend the range of the projectile. ALTERNATE FIRE to add up to two bounces to this arrow.', 'Recon Bolt', 'uploads/agents/abilities/reconbolt.png', 'EQUIP a bow with recon bolt. FIRE to send the recon bolt forward, activating upon collision and revealing the location of nearby enemies caught in the line of sight of the bolt. Enemies can destroy this bolt. HOLD FIRE to extend the range of the projectil', 'Owl Drone', 'uploads/agents/abilities/owldrone.png', 'EQUIP an owl drone. FIRE to deploy and take control of movement of the drone. While in control of the drone, FIRE to shoot a marking dart. This dart will reveal the location of any player struck by the dart.', 'Hunters Fury', 'uploads/agents/abilities/huntersfury.png', 'EQUIP a bow with three long-range, wall-piercing energy blasts. FIRE to release an energy blast in a line in front of Sova, dealing damage and revealing the location of enemies caught in the line. This ability can be RE-USED up to two more times while the', '2021-05-29 09:13:21', '2021-05-29 09:13:21'),
(75, 'uploads/agents/viper.png', 'Viper', 'Controllers', 'The American Chemist, Viper deploys an array of poisonous chemical devices to control the battlefield and cripple the enemy\'s vision. If the toxins don\'t kill her prey, her mindgames surely will.', 'Poison Cloud', 'uploads/agents/abilities/poisoncloud.png', 'EQUIP a gas emitter. FIRE to throw the emitter that perpetually remains throughout the round. RE-USE the ability to create a toxic gas cloud at the cost of fuel. This ability can be RE-USED more than once and can be picked up to be REDEPLOYED.', 'Toxic Screen', 'uploads/agents/abilities/toxicscreen.png', 'EQUIP a gas emitter launcher that penetrates terrain. FIRE to deploy a long line of gas emitters. RE-USE the ability to create a tall wall of toxic gas at the cost of fuel. This ability can be RE-USED more than once.', 'Snake Bite', 'uploads/agents/abilities/snakebite.png', 'EQUIP a chemical launcher. FIRE to launch a canister that shatters upon hitting the floor, creating a lingering chemical zone that damages and applies Vulnerable.', 'Vipers Pit', 'uploads/agents/abilities/viperspit.png', 'EQUIP a chemical sprayer. FIRE to spray a chemical cloud in all directions around Viper, creating a large cloud that reduces the vision range of players and maximum health of enemies inside of it. HOLD the ability key to disperse the cloud early.', '2021-05-29 09:16:20', '2021-05-29 09:16:20'),
(76, 'uploads/agents/phoenix.png', 'Phoenix', 'Duelists', 'Hailing from the U.K., Phoenix\'s star power shines through in his fighting style, igniting the battlefield with flash and flare. Whether he\'s got backup or not, he\'s rushing in to fight on his own terms.', 'Blaze', 'uploads/agents/abilities/blaze.png', 'EQUIP a flame wall. FIRE to create a line of flame that moves forward, creating a wall of fire that blocks vision and damages players passing through it. HOLD FIRE to bend the wall in the direction of your crosshair.', 'Curveball', 'uploads/agents/abilities/curveball.png', 'EQUIP a flare orb that takes a curving path and detonates shortly after throwing. FIRE to curve the flare orb to the left, detonating and blinding any player who sees the orb. ALTERNATE FIRE to curve the flare orb to the right.', 'Hot Hands', 'uploads/agents/abilities/hothands.png', 'EQUIP a fireball. FIRE to throw a fireball that explodes after a set amount of time or upon hitting the ground, creating a lingering fire zone that damages enemies.', 'Run it Back', 'uploads/agents/abilities/runitback.png', 'INSTANTLY place a marker at Phoenix\'s location. While this ability is active, dying or allowing the timer to expire will end this ability and bring Phoenix back to this location with full health.', '2021-05-29 09:18:13', '2021-05-29 09:18:13'),
(77, 'uploads/agents/brimstone.png', 'Brimstone', 'Controllers', 'Joining from the USA, Brimstone\'s orbital arsenal ensures his squad always has the advantage. His ability to deliver utility precisely and safely make him the unmatched boots-on-the-ground commander.', 'Stim Beacon', 'uploads/agents/abilities/stimbeacon.png', 'INSTANTLY toss a stim beacon in front of Brimstone. Upon landing, the stim beacon will create a field that grants players RapidFire.', 'Incendiary', 'uploads/agents/abilities/incendiary.png', 'EQUIP an incendiary grenade launcher. FIRE to launch a grenade that detonates as it comes to a rest on the floor, creating a lingering fire zone that damages players within the zone.', 'Sky Smoke', 'uploads/agents/abilities/skysmoke.png', 'EQUIP a tactical map. FIRE to set locations where Brimstone\'s smoke clouds will land. ALTERNATE FIRE to confirm, launching long-lasting smoke clouds that block vision in the selected area.', 'Orbital Strike', 'uploads/agents/abilities/orbitalstrike.png', 'EQUIP a tactical map. FIRE to launch a lingering orbital strike laser at the selected location, dealing high damage-over-time to players caught in the selected area.', '2021-05-29 09:20:59', '2021-05-29 09:31:52'),
(78, 'uploads/agents/sage.png', 'Sage', 'Sentinels', 'The bastion of China, Sage creates safety for herself and her team wherever she goes. Able to revive fallen friends and stave off forceful assaults, she provides a calm center to a hellish battlefield.', 'Slow Orb', 'uploads/agents/abilities/sloworb.png', 'EQUIP a slowing orb. FIRE to throw a slowing orb forward that detonates upon landing, creating a lingering field that slows players caught inside of it.', 'Healing Orb', 'uploads/agents/abilities/healingorb.png', 'EQUIP a healing orb. FIRE with your crosshairs over a damaged ally to activate a heal-over-time on them. ALT FIRE while Sage is damaged to activate a self heal-over-time.', 'Barrier Orb', 'uploads/agents/abilities/barrierorb.png', 'EQUIP a barrier orb. FIRE places a wall that fortifies after a few seconds. ALT FIRE rotates the targeter.', 'Resurrection', 'uploads/agents/abilities/resurrection.png', 'EQUIP a resurrection ability. FIRE with your crosshairs placed over a dead ally to begin resurrecting them. After a brief channel, the ally will be brought back to life with full health.', '2021-05-29 09:23:49', '2021-05-29 09:23:49'),
(79, 'uploads/agents/reyna.png', 'Reyna', 'Duelists', 'Forged in the heart of Mexico, Reyna dominates single combat, popping off with each kill she scores. Her capability is only limited by her raw skill, making her sharply dependant on performance.', 'Devour', 'uploads/agents/abilities/devour.png', 'Soul Harvest: Enemies that die to Reyna, or die within 3 seconds of taking damage from Reyna, leave behind Soul Orbs that last 3 seconds.\r\nDevour: INSTANTLY consume a nearby soul orb, rapidly healing for a short duration. Health gained through this skill ', 'Dismiss', 'uploads/agents/abilities/dismiss.png', 'INSTANTLY consume a nearby Soul Orb, becoming intangible for a short duration. If EMPRESS is active, also become invisible.', 'Leer', 'uploads/agents/abilities/leer.png', 'EQUIP an ethereal, destructible eye. ACTIVATE to cast the eye a short distance forward. The eye will Nearsight all enemies who look at it.', 'Empress', 'uploads/agents/abilities/empress.png', 'INSTANTLY enter a frenzy, increasing firing, equip and reload speed dramatically. Gain infinite charges of Soul Harvest abilities. When an enemy dies to Reyna, or dies within 3 seconds of taking damage from Reyna, the duration is renewed.', '2021-05-29 09:26:26', '2021-05-29 09:26:26'),
(80, 'uploads/agents/omen.png', 'Omen', 'Controllers', 'A phantom of a memory, Omen hunts in the shadows. He renders enemies blind, teleports across the field, then lets paranoia take hold as his foe scrambles to uncover where he might strike next.', 'Paranoia', 'uploads/agents/abilities/paranoia.png', 'EQUIP a blinding orb.  FIRE to throw it forward, briefly reducing the vision range and deafening all players it touches. This projectile can pass straight through walls.', 'Dark Cover', 'uploads/agents/abilities/darkcover.png', 'EQUIP a shadow orb, entering a phased world to place and target the orbs. PRESS the ability key to throw the shadow orb to the marked location, creating a long-lasting shadow sphere that blocks vision. HOLD FIRE while targeting to move the marker further ', 'Shrouded Step', 'uploads/agents/abilities/shroudedstep.png', 'EQUIP a shrouded step ability and see its range indicator. FIRE to begin a brief channel, then teleport to the marked location.', 'From the Shadows', 'uploads/agents/abilities/fromtheshadows.png', 'EQUIP a tactical map. FIRE to begin teleporting to the selected location. While teleporting, Omen will appear as a Shade that can be destroyed by an enemy to cancel his teleport, or PRESS EQUIP for Omen to cancel his teleport.', '2021-05-29 09:29:01', '2021-05-29 09:29:01'),
(81, 'uploads/agents/skye.png', 'Skye', 'Initiators', 'Hailing from Australia, Skye and her band of beasts trailblaze the way through hostile territory. With her creations hampering the enemy, and her power to heal others, the team is strongest and safest by Skye\'s side.', 'Trailblazer', 'uploads/agents/abilities/trailblazer.png', 'EQUIP a Tasmanian tiger trinket. FIRE to send out and take control of the predator.  While in control, FIRE to leap forward, exploding in a concussive blast and damaging directly hit enemies.', 'Guiding Light', 'uploads/agents/abilities/guidinglight.png', 'EQUIP a hawk trinket.  FIRE to send it forward.  HOLD FIRE to guide the hawk in the direction of your crosshair. RE-USE while the hawk is in flight to transform it into a flash.', 'Regrowth', 'uploads/agents/abilities/regrowth.png', 'EQUIP a healing trinket.  HOLD FIRE to channel, healing allies in range and line of sight.  Can be reused until her healing pool is depleted.  Skye cannot heal herself.', 'Seekers', 'uploads/agents/abilities/seekers.png', 'EQUIP a Seeker trinket.  FIRE to send out three Seekers to track down the three closest enemies.  If a Seeker reaches its target, it nearsights them.', '2021-05-29 09:35:40', '2021-05-29 09:37:47'),
(82, 'uploads/agents/killjoy.png', 'Killjoy', 'Sentinels', 'The genius of Germany, Killjoy secures and defends key battlefield positions with a collection of traps, turrets, and mines. Each invention is primed to punish any assailant too dumb to back down.', 'Nanoswarm', 'uploads/agents/abilities/nanoswarm.png', 'EQUIP a Nanoswarm grenade. FIRE to throw the grenade. Upon landing, the Nanoswarm goes covert. ACTIVATE the Nanoswarm to deploy a damaging swarm of nanobots.', 'ALARMBOT', 'uploads/agents/abilities/alarmbot.png', 'EQUIP a covert Alarmbot. FIRE to deploy a bot that hunts down enemies that get in range.  After reaching its target, the bot explodes and applies Vulnerable to enemies in the area. HOLD EQUIP to recall a deployed bot.', 'TURRET', 'uploads/agents/abilities/turret.png', 'EQUIP a Turret. FIRE to deploy a turret that fires at enemies in a 180 degree cone. HOLD EQUIP to recall the deployed turret.', 'Lockdown', 'uploads/agents/abilities/lockdown.png', 'EQUIP the Lockdown device. FIRE to deploy the device. After a long windup, the device Detains all enemies caught in the radius. The device can be destroyed by enemies.', '2021-05-29 09:41:30', '2021-05-29 09:41:30'),
(83, 'uploads/agents/astra.png', 'Astra', 'Controllers', 'Ghanaian Agent Astra harnesses the energies of the cosmos to reshape battlefields to her whim. With full command of her astral form and a talent for deep strategic foresight, she\'s always eons ahead of her enemy\'s next move.', 'Nova Pulse', 'uploads/agents/abilities/novapulse.png', 'Place Stars in Astral Form (X). ACTIVATE a Star to detonate a Nova Pulse. The Nova Pulse charges briefly then strikes, concussing all players in its area.', 'Nebula / Dissipate', 'uploads/agents/abilities/nebuladissipate.png', 'Place Stars in Astral Form (X).  ACTIVATE a Star to transform it into a Nebula (smoke). USE (F) a Star to Dissipate it, returning the star to be placed in a new location after a delay. Dissipate briefly forms a fake Nebula at the Star\'s location before re', 'Gravity Well', 'uploads/agents/abilities/gravitywell.png', 'Place Stars in Astral Form (X). ACTIVATE a Star to form a Gravity Well. Players in the area are pulled toward the center before it explodes, making all players still trapped inside vulnerable.', 'Astral Form / Cosmic Divide', 'uploads/agents/abilities/astralformcosmicdivide.png', 'ACTIVATE to enter Astral Form where you can place Stars with PRIMARY FIRE. Stars can be reactivated later, transforming them into a Nova Pulse, Nebula, or Gravity Well. When Cosmic Divide is charged, use SECONDARY FIRE in Astral Form to begin aiming it, t', '2021-05-29 09:46:26', '2021-05-29 09:46:26'),
(84, 'uploads/agents/yoru.png', 'Yoru', 'Duelists', 'Yoru infiltrates enemy lines and gains positional advantages in combat', 'FAKEOUT', 'uploads/agents/abilities/fakeout.png', 'EQUIP an echo that mimics footsteps when activated FIRE to activate and send the echo forward ALT FIRE to place an echo in place USE the inactive echo to send it forward.', 'BLINDSIDE', 'uploads/agents/abilities/blindside.png', 'EQUIP to rip an unstable dimensional fragment from reality. FIRE to throw the fragment, activating a flash that winds up once it collides with a hard surface in world.', 'GATECRASH', 'uploads/agents/abilities/gatecrash.png', 'EQUIP to harness a rift tether FIRE to send the tether out moving forward ALT FIRE to place a tether in place ACTIVATE to teleport to the tether\'s location.', 'DIMENSIONAL DRIFT', 'uploads/agents/abilities/dimensionaldrift.png', 'EQUIP a mask that can see between dimensions FIRE to drift into Yoru\'s dimension, unable to be affected or seen by enemies from the outside.', '2021-05-29 09:49:20', '2021-05-29 09:49:20');

-- --------------------------------------------------------

--
-- Table structure for table `maps`
--

CREATE TABLE `maps` (
  `id` int(11) NOT NULL,
  `splash` varchar(255) NOT NULL,
  `display` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `coordinate` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `maps`
--

INSERT INTO `maps` (`id`, `splash`, `display`, `name`, `coordinate`, `created_at`, `updated_at`) VALUES
(18, 'uploads/maps/ascent.png', 'uploads/maps/ascent_display.png', 'Ascent', '45°26\'BF\'N,12°20\'Q\'E', '2021-05-29 10:05:24', '2021-05-29 10:05:24'),
(19, 'uploads/maps/split.png', 'uploads/maps/split_display.png', 'Split', '35°41\'CD\'N,139°41\'WX\'E', '2021-05-29 10:06:06', '2021-05-29 10:06:06'),
(20, 'uploads/maps/bind.png', 'uploads/maps/bind_display.png', 'Bind', '34°2\'A\'N,6°51\'Z\'W', '2021-05-29 10:06:33', '2021-05-29 10:06:33'),
(21, 'uploads/maps/breeze.png', 'uploads/maps/breeze_display.png', 'Breeze', 'Unknown', '2021-05-29 10:07:04', '2021-05-29 10:07:04'),
(22, 'uploads/maps/icebox.png', 'uploads/maps/icebox_display.png', 'Icebox', '76°44\' A\'N 149°30\' Z\'E', '2021-05-29 10:07:40', '2021-05-29 10:07:40'),
(23, 'uploads/maps/haven.png', 'uploads/maps/haven_display.png', 'Haven', '27°28\'A\'N,89°38\'WZ\'E', '2021-05-29 10:08:28', '2021-05-29 10:08:28');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `role_id`, `name`, `email`, `password`, `created_at`, `updated_at`) VALUES
(14, 0, 'Rivaltino Arron', 'arron2501@gmail.com', '21232f297a57a5a743894a0e4a801fc3', '2021-05-29 08:32:50', '2021-05-29 08:35:18');

-- --------------------------------------------------------

--
-- Table structure for table `weapons`
--

CREATE TABLE `weapons` (
  `id` int(11) NOT NULL,
  `img` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `pfr` varchar(50) NOT NULL,
  `afr` varchar(50) NOT NULL,
  `body_dmg` int(11) NOT NULL,
  `head_dmg` int(11) NOT NULL,
  `leg_dmg` int(11) NOT NULL,
  `mag` int(11) NOT NULL,
  `wp` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `weapons`
--

INSERT INTO `weapons` (`id`, `img`, `name`, `category`, `pfr`, `afr`, `body_dmg`, `head_dmg`, `leg_dmg`, `mag`, `wp`, `created_at`, `updated_at`) VALUES
(7, 'uploads/weapons/classic.png', 'Classic', 'Sidearms', '6.75', 'None', 26, 78, 22, 12, 'Low', '2021-05-29 10:23:27', '2021-05-29 10:24:46'),
(8, 'uploads/weapons/ghost.png', 'Ghost', 'Sidearms', '6.75', 'None', 30, 105, 25, 15, 'Medium', '2021-05-29 10:24:20', '2021-05-29 10:24:20'),
(9, 'uploads/weapons/shorty.png', 'Shorty', 'Sidearms', '3.33', 'None', 12, 24, 10, 2, 'Low', '2021-05-29 10:25:34', '2021-05-29 10:25:34'),
(10, 'uploads/weapons/frenzy.png', 'Frenzy', 'Sidearms', '10', 'None', 26, 78, 22, 13, 'Low', '2021-05-29 10:26:04', '2021-05-29 10:26:04'),
(11, 'uploads/weapons/sheriff.png', 'Sheriff', 'Sidearms', '4', 'None', 55, 160, 47, 6, 'High', '2021-05-29 10:26:46', '2021-05-29 10:26:46'),
(12, 'uploads/weapons/stinger.png', 'Stinger', 'SMGs', '16', 'None', 27, 67, 23, 20, 'Low', '2021-05-29 10:27:32', '2021-05-29 10:27:32'),
(13, 'uploads/weapons/spectre.png', 'Spectre', 'SMGs', '13', '12', 26, 78, 22, 30, 'Low', '2021-05-29 10:28:11', '2021-05-29 10:28:11'),
(14, 'uploads/weapons/bulldog.png', 'Bulldog', 'Rifles', '9', '6', 35, 115, 30, 24, 'Medium', '2021-05-29 10:29:04', '2021-05-29 10:29:04'),
(15, 'uploads/weapons/guardian.png', 'Guardian', 'Rifles', '5', '4', 65, 195, 49, 12, 'High', '2021-05-29 10:29:43', '2021-05-29 10:29:43'),
(16, 'uploads/weapons/phantom.png', 'Phantom', 'Rifles', '11', '10', 39, 156, 33, 30, 'Medium', '2021-05-29 10:30:20', '2021-05-29 10:30:20'),
(17, 'uploads/weapons/vandal.png', 'Vandal', 'Rifles', '10', '9', 40, 160, 34, 25, 'Medium', '2021-05-29 10:30:52', '2021-05-29 10:30:52'),
(18, 'uploads/weapons/bucky.png', 'Bucky', 'Shotguns', '1', 'None', 20, 40, 17, 5, 'Low', '2021-05-29 10:31:25', '2021-05-29 10:31:25'),
(19, 'uploads/weapons/judge.png', 'Judge', 'Shotguns', '3', 'None', 17, 34, 14, 7, 'Low', '2021-05-29 10:31:58', '2021-05-29 10:31:58'),
(20, 'uploads/weapons/ares.png', 'Ares', 'Machine Guns', '10', '10', 30, 72, 25, 50, 'High', '2021-05-29 10:32:34', '2021-05-29 10:32:34'),
(21, 'uploads/weapons/odin.png', 'Odin', 'Machine Guns', '12', '17', 38, 95, 32, 100, 'High', '2021-05-29 10:33:06', '2021-05-29 10:33:06'),
(22, 'uploads/weapons/marshal.png', 'Marshal', 'Sniper Rifles', '1', '1', 101, 202, 85, 5, 'Medium', '2021-05-29 10:33:43', '2021-05-29 10:33:43'),
(23, 'uploads/weapons/operator.png', 'Operator', 'Sniper Rifles', '1', '1', 150, 255, 120, 5, 'High', '2021-05-29 10:34:16', '2021-05-29 10:34:16'),
(24, 'uploads/weapons/tacticalknife.png', 'Tactical Knife', 'Melee', 'None', 'None', 50, 0, 0, 0, 'None', '2021-05-29 10:35:23', '2021-05-29 10:35:23');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agents`
--
ALTER TABLE `agents`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `maps`
--
ALTER TABLE `maps`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `weapons`
--
ALTER TABLE `weapons`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agents`
--
ALTER TABLE `agents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `maps`
--
ALTER TABLE `maps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `weapons`
--
ALTER TABLE `weapons`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
