import FWCore.ParameterSet.Config as cms
import math

#common stuff here
det1 = 203.827   #position of first tracker detector
det2 = 212.550
tof  = 215.7   #position of time of flight detector
trklen = 10.
hit_smear= True
Ang_smear= True
E_smear = True
vtx_smear = False
run_with_CR = True
useCR = True
ecms = 13000.
det1xoffset = 0.
det2xoffset = 0.
phi_min = -math.pi
phi_max =  math.pi

VertexX = cms.double(0.)
VertexY = cms.double(0.)
VertexZ = cms.double(0.)

def customise(process):
	######## CTPPS
	process.load('PhysicsTools.HepMCCandAlgos.genParticles_cfi')
        process.load("FWCore.MessageLogger.MessageLogger_cfi")
        process.MessageLogger = cms.Service("MessageLogger")

	if hasattr(process.VtxSmeared,"X0"):
           VertexX = process.VtxSmeared.X0
           VertexY = process.VtxSmeared.Y0
           VertexZ = process.VtxSmeared.Z0

        if hasattr(process.VtxSmeared,"MeanX"):
           VertexX = process.VtxSmeared.MeanX
           VertexY = process.VtxSmeared.MeanY
           VertexZ = process.VtxSmeared.MeanZ



	print 'Setting CT-PPS FastSim'
	ppssim_beam_options = cms.PSet(
  			Verbosity = cms.untracked.int32(0),
               	         Beam1File = cms.FileInPath("FastSimulation/PPSFastSim/data/LHCB1_Beta0.40_6.5TeV_CR205_v6.503.tfs"),
                         Beam2File = cms.FileInPath("FastSimulation/PPSFastSim/data/LHCB2_Beta0.40_6.5TeV_CR205_v6.503.tfs"),
                         Beam1Direction = cms.int32(1),
                         Beam2Direction = cms.int32(1),
                         SmearEnergy    = cms.bool(E_smear),
                         SmearAngle     = cms.bool(Ang_smear),
                         BeamEnergy     = cms.double(ecms/2.0),
                         BeamEnergyRMS  = cms.double(1.11e-4),
                         BeamAngleRMS   = cms.double(30.03), # in mrad
                         BeamSizeAtTrk1 = cms.double(0.186), # beam sigma (X) at first  tracker station in mm
                         BeamSizeAtTrk2 = cms.double(0.115), # beam sigma (X) at second tracker station in mm
                         BeamSizeAtToF  = cms.double(0.113), # beam sigma (X) at timing station in mm
                         ShowBeamLine   = cms.untracked.bool(False),
                         SimBeamProfile = cms.untracked.bool(False),
                         CrossAngleCorr = cms.bool(useCR),
                         CrossingAngle  = cms.double(205.0) #in mrad
                         )
	ppssim_tofDiamond = cms.PSet(
                         ToFGeometry       = cms.string("diamond"),
                         ToFCellWidth      = cms.untracked.vdouble(0.81, 0.91, 1.02, 1.16, 1.75, 2.35, 4.2, 4.2), # tof cell width in mm #move to vector - diamond geometry
                         ToFCellHeight     = cms.double(4.2), # tof cell height in mm
                         ToFNCellX         = cms.int32(8),      # number of cells in X
                         ToFNCellY         = cms.int32(1),      # number of cells in Y
                         )
	ppssim_tofQuartz = cms.PSet(
                         ToFGeometry       = cms.string("quartz"),
                         ToFCellWidth      = cms.untracked.vdouble(3.0), # tof cell width in mm #move to vector - diamond geometry
                         ToFCellHeight     = cms.double(3.0), # tof cell height in mm
                         ToFNCellX         = cms.int32(5),      # number of cells in X
                         ToFNCellY         = cms.int32(4),      # number of cells in Y
                         )
	ppssim_detector_options = cms.PSet(
                         TrackerWidth      = cms.double(20.0), # tracker width in mm
                         TrackerHeight     = cms.double(18.0), # tracker height in mm
                         ToFPitchX         = cms.double(100),  # pitch between cells in X in microns
                         ToFPitchY         = cms.double(100),  # pitch between cells in Y in microns
                         TrackerInsertion  = cms.double(15), # Number of sigmas (X) from the beam for the tracker
                         ToFInsertion      = cms.double(15), # Number of sigmas (X) from the beam for the tof
                         TrackerZPosition  = cms.double(det1),
                         TrackerLength     = cms.double(trklen),
                         TrkDet1XOffset    = cms.double(det1xoffset), # tracker 1 missalignment
                         TrkDet2XOffset    = cms.double(det2xoffset), # tracker 2 missalignment
                         ToFZPosition      = cms.double(tof),
                         SmearHit          = cms.bool(hit_smear),
                         HitSigmaX         = cms.double(10),
                         HitSigmaY         = cms.double(10),
                         HitSigmaZ         = cms.double(0),
                         TimeSigma         = cms.double(0.01), #in ns
                         MinThetaXatDet1   = cms.double(-500.), #min. theta x at first tracker in urad
                         MaxThetaXatDet1   = cms.double(500.),   #max. theta x at first tracker in urad
                         MinThetaYatDet1   = cms.double(-500.), #min. theta y at first tracker in urad
                         MaxThetaYatDet1   = cms.double(500.), #max. theta y at first tracker in urad
                         DetectorClosestX  = cms.double(-2.),  #min. distance to the beam EVER
                         MaxXfromBeam      = cms.double(-25),  #max. x from beam for a hit EVER
                         MaxYfromBeam      = cms.double(10.),  #max |y| from beam for a hit EVER
                         FilterHitMap      = cms.bool(True),    #apply geometrical (X,Y) in the hits
                         ApplyFiducialCuts = cms.bool(True)     #apply geometrical (X,Y) in the hits
                         )

	ppssim_general_options = cms.PSet(
                         UseHepMCProducer = cms.untracked.bool(True), 
            	         VtxMeanX       = VertexX,
                         VtxMeanY       = VertexY,
                         VtxMeanZ       = VertexZ,
                         CollisionPoint = cms.string("IP5"),
                         TCL4Position    = cms.untracked.double(143.0),
                         TCL5Position    = cms.untracked.double(183.8),
                         TCL6Position    = cms.untracked.double(221.6),
                         PhiMin          = cms.double(phi_min),
                         PhiMax          = cms.double(phi_max),
                         CentralMass     = cms.double(125.7),
                         CentralMassErr  = cms.double(0.4),
                         EtaMin          = cms.double(7.0),  # min eta to be tracked by HECTOR
                         MomentumMin     = cms.double(3.000), # min mom. to be tracked by HECTOR
                         TrackImpactParameterCut = cms.double(0.5) # max. imp. par. for reco tracks
			 )


	process.ppssim = cms.EDProducer('PPSProducer',
					ppssim_beam_options,
                    ppssim_tofDiamond,
                    #ppssim_tofQuartz,
                    ppssim_detector_options,
                    ppssim_general_options,
					genSource = cms.InputTag("generatorSmeared") # for HepMC event -> no pileup events
					)

	# Adding CT-PPS 
	process.AODSIMoutput.outputCommands.extend(cms.untracked.vstring('keep PPSGenDataPPSSpectrometer_*_*_*','keep PPSSimDataPPSSpectrometer_*_*_*','keep PPSRecoDataPPSSpectrometer_*_*_*'))## add CTPPS eventContent
	# Path and EndPath definitions
	process.ppssim_step = cms.Path(process.generator+process.ppssim)#CTPPS
	process.generation_step.replace(process.generator,process.generator * process.VtxSmeared)#CTPPS

	# CMSSW_7_6_0_pre1 or greather 
 	process.schedule.insert(6,process.ppssim_step)	

	return (process)

def customise_pu_protons_ctpps(process):
	
	process=customise(process)
        
	process.mix.mixObjects.mixHepMC.makeCrossingFrame = cms.untracked.bool(True)

	process.ppssim.UseHepMCProducer = cms.untracked.bool(False)
	# PU gen particle   		
	process.genParticlesPU = cms.EDProducer("GenParticleProducer",
	saveBarCodes = cms.untracked.bool(True),
	mix = cms.string("mix"),
	abortOnUnknownPDGCode = cms.untracked.bool(False),
	useCrossingFrame = cms.untracked.bool(True)
	)
	process.genProtonsPU = cms.EDFilter("GenParticleSelector",
		filter = cms.bool(False),
		src = cms.InputTag("genParticlesPU"),
		cut = cms.string('')
	)

	process.genProtonsPU.cut = 'status = 1 & pdgId == 2212 & abs(pz) >= %f' % ( 0.5*13000./2.0)
	outputCommandsPU = [ 'keep *_genParticlesPU_*_*', 'keep *_genProtonsPU_*_*']
	
	process.ppssim.genSource = cms.InputTag("genProtonsPU") # for Pile-up events

	process.digitisation_step.replace(process.pdigi_valid, process.pdigi_valid * process.genParticlesPU * process.genProtonsPU)

	return (process)
