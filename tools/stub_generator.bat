@echo off
title Stub Generator
echo Generating AI Stubs
ppython stub_generator.py --type AI dc ../astron/dclass/otp.dc ../astron/dclass/pirates.dc
echo Generating UD Stubs
ppython stub_generator.py --type UD dc ../astron/dclass/otp.dc ../astron/dclass/pirates.dc
echo Done!
pause
